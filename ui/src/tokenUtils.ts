import type { AxiosRequestConfig } from "axios";
import Cookies from "js-cookie";

const sessionStartStorageKey = "sessionStart";

function hasAccessTokenExpired(
    sessionStart: number,
    maxTokenLifetime: number
): boolean {
    return Date.now() > sessionStart + maxTokenLifetime;
}

/**
 * Sets the start time for this session.
 * This is used to detect if the access token
 * may have expired.
 */
export function setSessionStartTime() {
    window.sessionStorage.setItem(sessionStartStorageKey, `${Date.now()}`);
}

function getSessionStartTime(): string | null {
    return window.sessionStorage.getItem(sessionStartStorageKey);
}

export function getRequestInterceptor(
    maxTokenLifetime: number,
    accessTokenCookieName: string,
    tenantSubDomainCookieName:string,
    refreshTokenCallback: () => Promise<void>,
    addAuthHeader = true
): (config: AxiosRequestConfig) => Promise<AxiosRequestConfig> {
    return async (config: AxiosRequestConfig) => {
        if (!config.url) {
            console.error("Making a request without a URL??");
            return config;
        }

        // Include the CSRF token for all requests to our own service.
        // Such URLs will be relative.
        if (config.url.startsWith("/")) {
            if (!config.headers) {
                config.headers = {};
            }

            config.headers["X-CSRF-Token"] = Cookies.get("X-CSRF-Token") || "";
        }

        // Don't intercept requests to the oauth2 endpoint since we would
        // make requests to refresh the token which uses a cookie that is
        // only available to the server. There is no Authorization header
        // to set for that.
        if (config.url.includes("oauth2") || config.url.includes("auth")) {
            return config;
        }

        let accessToken = Cookies.get(accessTokenCookieName);
        const sessionStart = getSessionStartTime();
        if (
            !accessToken ||
            sessionStart === null ||
            !sessionStart ||
            hasAccessTokenExpired(parseInt(sessionStart, 10), maxTokenLifetime)
        ) {
            // Try to refresh the token first.
            await refreshTokenCallback();

            // This won't be reached if the refresh token cookie is not
            // available to the server because it, too, has expired/not available
            // and the server redirects the browser to login again.
            // The server would return a 401 status code which will
            // be handled by the response interceptor below.
            setSessionStartTime();

            // Now try to get the access token from the cookies again.
            // If there is still no access token, that's ok, the response would be
            // a 401, which will cause the user to re-login.
            accessToken = Cookies.get(accessTokenCookieName);
            if (!accessToken) {
                return config;
            }
        }

        if (!addAuthHeader) {
            return config;
        }

        if (!config.headers) {
            config.headers = {};
        }

        config.headers["Authorization"] = `Bearer ${accessToken}`;
        config.headers["sfmc_tssd"] = tenantSubDomainCookieName;

        return config;
    };
}
