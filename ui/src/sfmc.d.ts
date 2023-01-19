declare module "sfmc" {
    export interface SfmcResponse<T> {
        count: number;
        page: number;
        pageSize: number;
        items: T[];
    }

    export interface AssetChannels {
        email: boolean;
        web: boolean;
    }

    export interface AssetType {
        name: string;
        id: number;
    }

    export interface Page {
        page: number;
        pageSize: number;
    }

    export type SimpleOperator =
        | "equal"
        | "notEqual"
        | "lessThan"
        | "lessThanOrEqual"
        | "greaterThan"
        | "greaterThanOrEqual"
        | "like"
        | "isNull"
        | "isNotNull"
        | "contains"
        | "mustcontain"
        | "startsWith"
        | "in"
        | "where";

    export interface Query {
        property: string;
        simpleOperator: SimpleOperator;
        value: string;
    }

    export type LogicalOperator = "AND" | "OR";

    export interface MultiQuery {
        leftOperand: MultiQuery | Query;
        logicalOperator?: LogicalOperator;
        rightOperand?: MultiQuery | Query;
    }

    export interface Sort {
        property: string;
        direction: "ASC" | "DESC";
    }

    export interface AssetQueryRequest {
        page: Page;
        query: MultiQuery | Query;
        sort?: Sort[];
        fields?: string[];
    }

    export interface HtmlEmailContent {
        content: string;
    }

    export interface AssetViews {
        html: HtmlEmailContent;
    }

    export interface User {
        id: number;
        email: string;
        name: string;
    }

    export type SharingType = "edit" | "local" | "view";

    export interface SharingProperties {
        sharedWith: number[];
        sharingType: SharingType;
    }

    export interface CreateAssetRequest {
        assetType: AssetType;
        channels: AssetChannels;
        customerKey: string;
        description?: string;
        name: string;
        views?: AssetViews;
        sharingProperties: SharingProperties;
        /**
         * Assets of type htmlblock must set this property instead of using views.
         */
        content?: string;
        category?: Partial<Category>;
    }

    export interface PatchAssetRequest {
        views?: AssetViews;
        /**
         * Assets of type htmlblock must set this property instead of using views.
         */
        content?: string;
    }

    export interface Thumbnail {
        thumbnailUrl?: string;
    }

    export interface Asset extends CreateAssetRequest {
        id: number;
        contentType: string;
        createdDate: string;
        createdBy: User;
        modifiedDate: string;
        modified: User;
        objectID: string;
        thumbnail?: Thumbnail;
    }

    export interface HtmlContentBlock extends Asset {
        content?: string;
    }

    export interface Category {
        id: number;

        enterpriseId: number;
        memberId: number;
        parentId: number;

        categoryType: "asset" | "asset-shared";
        description: string;
        name: string;
    }

    export interface Organization {
        // We are only interested in a limited set of properties.
        // There are a lot more properties returned in the response.
        member_id: number;
        enterprise_id: number;
    }

    export interface OrgRestEndpoints {
        rest_instance_url: string;
        soap_instance_url: string;
    }

    export interface User {
        // We are only interested in a limited set of properties.
        // There are a lot more properties returned in the response.
        email: string;
    }

    // We are only interested in the organization's MID in this app
    // right now. So we'll omit the other properties that we can access
    // from the raw response.
    // https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/getUserInfo.html
    export interface UserInfo {
        organization: Organization;
        rest: OrgRestEndpoints;
        user: User;
    }
}
