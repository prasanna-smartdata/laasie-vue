import * as axios from "axios";
import type { SfmcS2sPayload } from "external-api";

import { getRequestInterceptor } from "./tokenUtils";

export const settings = {
    apiBaseUrl: "/api/laasie",
    accessTokenCookieName: "external_access_token",
    tokenRefreshInterval: 50 * 60 * 1000,
    maxTokenLifetime: 60 * 60 * 1000,
};

export const client = axios.default.create({
    baseURL: 'http://app.localhost',
    timeout: 30 * 1000,
});
// Add a request interceptor so that we can set the
// access token in the Authorization header for every
// request to the API.
client.interceptors.request.use(
    getRequestInterceptor(
        settings.maxTokenLifetime,
        settings.accessTokenCookieName,
        "",
        refreshExternalToken
    )
);

export async function refreshExternalToken() {
    try {
        // TODO: Fix the path of the refresh token endpoint implemented
        // by our API backend to handle the customer's OAuth2 flow.
        // The customer's OAuth flow is NOT the SFMC OAuth flow.
        await client.post("/auth/laasie/token");
        setTimeout(refreshExternalToken, settings.tokenRefreshInterval);
    } catch (err) {
        console.error(
            "Error occurred while trying to refresh the token. Won't schedule the auto refresh."
        );
        console.error(err);
    }
}

/**
 * Calls the backend API's token endpoint for Laasie.
 * This initializes the access token cookie that is
 * only accessible from the API backend (the Python code).
 */
export async function initLaasieApiAccessToken(): Promise<void> {
    await client.post("/auth/laasie/token", { timeout: 10 });
}

export async function saveSfmcS2sCredentials(
    payload: SfmcS2sPayload
): Promise<void> {
    const response = await client.post(`${settings.apiBaseUrl}/sfmc`, payload);

    return response.data;
}
