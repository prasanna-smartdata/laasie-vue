import * as axios from "axios";

import type {
    Category,
    Asset,
    AssetQueryRequest,
    CreateAssetRequest,
    HtmlContentBlock,
    PatchAssetRequest,
    Query,
    SfmcResponse,
    UserInfo,
} from "sfmc";
import { getRequestInterceptor } from "./tokenUtils";

export const settings = {
    sfmcBaseApiUrlSuffix: "rest.marketingcloudapis.com",
    accessTokenCookieName: "sfmc_access_token",
    tenantSubDomainCookieName: "sfmc_tssd",
    tokenRefreshInterval: 15 * 60 * 1000,
    maxTokenLifetime: 20 * 60 * 1000,
};

/**
 * The Content Builder category where we expect users to create
 * custom HTML blocks as templates to insert a suggested article
 * into the email template.
 *
 * IMPORTANT! Changing this has implications for existing users.
 * Existing users would have to move any HTML blocks they had in
 * the previous category into the new one if this was changed.
 */
export const defaultCategoryName = "Laasie Collection Templates";

const client = axios.default.create({
    timeout: 20 * 1000,
});

// Add a request interceptor so that we can set the
// access token in the Authorization header for every
// request to the API.
client.interceptors.request.use(
    getRequestInterceptor(
        settings.maxTokenLifetime,
        settings.accessTokenCookieName,
        refreshSfmcToken,
        false
    )
);

client.interceptors.response.use(undefined, (err) => {
    if (err.response.status === 401) {
        window.location.href = "/oauth2/sfmc/authorize";
        return;
    }

    return Promise.reject(err);
});

export async function refreshSfmcToken() {
    try {
        await client.post("/oauth2/sfmc/refresh_token");
        setTimeout(refreshSfmcToken, settings.tokenRefreshInterval);
    } catch (err) {
        console.error(
            "Error occurred while trying to refresh the token. Won't schedule the auto refresh."
        );
        console.error(err);
    }
}

export async function getAssetByCustomerKey(
    name: string
): Promise<Asset | undefined> {
    try {
        const response = await client.get<SfmcResponse<Asset>>(
            "/api/sfmc/asset/v1/content/assets",
            {
                params: {
                    $filter: `customerKey eq '${name}'`,
                },
            }
        );
        if (!response.data.count) {
            return;
        }

        return response.data.items[0];
    } catch (err) {
        console.error("Failed to fetch asset by name", name);
        throw err;
    }
}

export async function listExistingHtmlBlocks(): Promise<HtmlContentBlock[]> {
    const assetTypeQuery: Query = {
        property: "assetType.name",
        simpleOperator: "equal",
        value: "htmlblock",
    };

    const categoryNameQuery: Query = {
        property: "category.name",
        simpleOperator: "equal",
        value: defaultCategoryName,
    };

    const body: AssetQueryRequest = {
        page: {
            page: 1,
            pageSize: 50,
        },
        query: {
            leftOperand: assetTypeQuery,
            logicalOperator: "AND",
            rightOperand: categoryNameQuery,
        },
    };
    try {
        const response = await client.post<SfmcResponse<HtmlContentBlock>>(
            "/api/sfmc/asset/v1/content/assets/query",
            body
        );
        return response.data.items;
    } catch (err) {
        console.error("Failed to list HTML blocks", err);
        throw err;
    }
}

async function createAsset(
    key: string,
    name: string,
    html: string,
    categoryId?: number
): Promise<void> {
    const body: CreateAssetRequest = {
        customerKey: key,
        name,
        // https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/base-asset-types.html
        assetType: {
            id: 197,
            name: "htmlblock",
        },
        channels: {
            email: true,
            web: false,
        },
        content: html,
        sharingProperties: {
            sharedWith: [0],
            sharingType: "edit",
        },
    };

    if (categoryId) {
        body.category = {
            id: categoryId,
        };
    }

    try {
        await client.post<Asset>("/api/sfmc/asset/v1/content/assets", body, {
            headers: {
                "Content-Type": "application/json",
            },
        });
    } catch (err) {
        const msg = "Failed to create the asset in Content Builder";
        console.error(msg, err);
        throw new Error(msg);
    }
}

async function updateAsset(assetId: number, html: string): Promise<void> {
    const body: PatchAssetRequest = {
        content: html,
    };

    try {
        await client.patch<Asset>(
            `/api/sfmc/asset/v1/content/assets/${assetId}`,
            body,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );
    } catch (err) {
        const msg = "Failed to update the asset";
        console.error(msg, err);
        throw new Error(msg);
    }
}

export async function listCategories(): Promise<Category[]> {
    const resp = await client.get<SfmcResponse<Category>>(
        "/api/sfmc/asset/v1/content/categories"
    );
    return resp.data.items;
}

// https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/createCategory.html
export async function createDefaultCategory(
    parentId: number
): Promise<Category> {
    const resp = await client.post<Category>(
        "/api/sfmc/asset/v1/content/categories",
        {
            parentId: parentId,
            name: defaultCategoryName,
            categoryType: "asset-shared",
            sharingProperties: {
                // Enable sharing across the entire enterprise.
                sharedWith: [0],
                // "edit" is the only possible value.
                sharingType: "edit",
            },
        },
        { headers: { "Content-Type": "application/json" } }
    );

    return resp.data;
}

export async function upsertAsset(
    key: string,
    name: string,
    html: string
): Promise<void> {
    const existingAsset = await getAssetByCustomerKey(key);
    if (!existingAsset) {
        await createAsset(key, name, html);
        return;
    }

    await updateAsset(existingAsset.id, html);
}

export async function getThumbnailBase64(
    thumbnailUrl: string
): Promise<string> {
    try {
        const response = await client.get<string>(
            `/api/sfmc/asset${thumbnailUrl}`
        );
        return `data:image/png;base64,${response.data}`;
    } catch (err) {
        console.error("Failed to fetch the thumbnail base64 string");
    }

    return "";
}

export async function getUserInfo(): Promise<UserInfo> {
    const response = await client.get<UserInfo>("/api/sfmc/userinfo");
    return response.data;
}
