<template>
    <LoadingSpinner v-if="loading" />

    <div class="slds-form-element">
        <div class="slds-m-top_xxx-small slds-float_top">
            <div
                id="foot"
                :class="showSuccess ? 'slds-is-expanded' : 'slds-is-collapsed'"
            >
                <div class="slds-notify_container slds-is-relative">
                    <div
                        class="slds-notify slds-notify_toast slds-theme_success"
                        role="status"
                    >
                        <span class="slds-assistive-text">success</span>
                        <span
                            class="slds-icon_container slds-icon-utility-success slds-m-right_small slds-no-flex slds-align-top"
                            title="Description of icon when needed"
                        >
                            <UtilityIcon
                                svgClass="slds-icon slds-icon_small"
                                iconName="success"
                            />
                        </span>
                        <div>
                            <div class="slds-text-heading_small">
                                SFMC App Credentials Verified{" "}
                            </div>
                        </div>
                        <div class="slds-notify__close">
                            <Button
                                class="slds-button slds-button_icon slds-button_icon-inverse"
                                title="Close"
                            >
                                <UtilityIcon
                                    svgClass="slds-button__icon slds-button__icon_large"
                                    iconName="close"
                                />
                                <span class="slds-assistive-text"> Close </span>
                            </Button>
                        </div>
                    </div>
                </div>
            </div>

            <div
                id="errorfoot"
                :class="showError ? 'slds-is-expanded' : 'slds-is-collapsed'"
            >
                <div class="slds-notify_container slds-is-relative">
                    <div
                        class="slds-notify slds-notify_toast slds-theme_error"
                        role="status"
                    >
                        <span class="slds-assistive-text">error</span>
                        <span
                            class="slds-icon_container slds-icon-utility-error slds-m-right_small slds-no-flex slds-align-top"
                            title="Description of icon when needed"
                        >
                            <UtilityIcon
                                svgClass="slds-icon slds-icon_small"
                                iconName="error"
                            />
                        </span>
                        <div class="slds-notify__content">
                            <h2 class="slds-text-heading_small">
                                {" "} Verification failed.Please check the
                                credentials
                            </h2>
                        </div>
                        <div class="slds-notify__close">
                            <button
                                class="slds-button slds-button_icon slds-button_icon-inverse"
                                title="Close"
                            >
                                <UtilityIcon
                                    svgClass="slds-button__icon slds-button__icon_large"
                                    iconName="close"
                                />
                                <span class="slds-assistive-text"> Close </span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="slds-theme_default">
            <div class="slds-text-heading_small slds-m-around_large">
                <img src="@/assets/images/laasie.png" width="120" height="100"/>
            </div>
            <div
                class="slds-box slds-text-heading_label slds-m-left_large slds-m-right_large"
            >
                <div class="slds-text-heading_small">
                    <img src="@/assets/images/logo.svg" width="40" height="30" />
                    <span class="slds-grid_vertical-align-start">
                        Server 2 Server Application Details
                    </span>
                </div>
            </div>

            <div class="slds-clearfix">
                <div class="slds-col slds-size_2-of-6">
                    <div class="slds-col_padded slds-m-left_none">
                        <div class="slds-col_padded">
                            <div class="slds-form-element">
                                <label
                                    class="slds-form-element__label"
                                    for="text-input-id-47"
                                >
                                    <abbr class="slds-required" title="required"
                                        >* </abbr
                                    >Client ID</label
                                >
                                <div class="slds-form-element__control">
                                    <input
                                        type="text"
                                        id="text-input-id-47"
                                        placeholder="Enter Client ID "
                                        required
                                        class="slds-input"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="slds-col_padded slds-m-left_none">
                        <div class="slds-col_padded">
                            <div class="slds-form-element">
                                <label
                                    class="slds-form-element__label"
                                    for="text-input-id-47"
                                >
                                    <abbr class="slds-required" title="required"
                                        >* </abbr
                                    >Client Secret</label
                                >
                                <div class="slds-form-element__control">
                                    <input
                                        type="text"
                                        id="text-input-id-47"
                                        placeholder="Enter Secret Key"
                                        required
                                        class="slds-input"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="slds-col_padded slds-m-left_none">
                        <div class="slds-col_padded">
                            <div class="slds-form-element">
                                <label
                                    class="slds-form-element__label"
                                    for="text-input-id-47"
                                >
                                    <abbr class="slds-required" title="required"
                                        >* </abbr
                                    >Customer ID</label
                                >
                                <div class="slds-form-element__control">
                                    <input
                                        type="text"
                                        id="text-input-id-47"
                                        placeholder="Enter Customer ID"
                                        required
                                        class="slds-input"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                    &nbsp;
                    <div class="slds-float_right slds-m-around--medium">
                        <button
                            class="slds-button slds-button_brand slds-m-right_x-small"
                            name="verify"
                        >
                            Verify My Account
                        </button>
                    </div>
                </div>

                <div class="slds-modal__footer slds-m-top--xx-large">
                    <button id="button" class="slds-button slds-button_neutral" :disabled="isValid">
                        Next
                    </button>
                </div>
            </div>
        </div>
    </div>

    <NotificationComponent
        :notifications="notifications"
        @on-notification-close="onNotificationClose"
    ></NotificationComponent>
</template>
<script lang="ts" setup>
import { ref } from "vue";

import NotificationComponent from "@/components/NotificationComponent.vue";
import type { NotificationContent } from "@/components/NotificationComponent.vue";
import LoadingSpinner from "@/components/LoadingSpinner.vue";

import { getUserInfo } from "@/sfmcClient";
import { saveSfmcS2sCredentials } from "@/externalApiClient";

const notifications = ref<NotificationContent[]>([]);
const loading = ref(false);
const clientId = ref<string>();
const clientSecret = ref<string>();

function getSubdomainFromRestUrl(sfmcRestUrl: string): string {
    const url = new URL(sfmcRestUrl);
    // SFMC REST API URLs always are of the format:
    // https://<tenant-subdomain>.auth.marketingcloudapis.com.
    return url.hostname.split(".")[0];
}

async function onSubmitClick() {
    if (!clientId.value || !clientSecret.value) {
        return;
    }

    loading.value = true;
    try {
        const userInfo = await getUserInfo();
        await saveSfmcS2sCredentials({
            CID: clientId.value,
            CSecret: clientSecret.value,
            Email: userInfo.user.email,
            MID: userInfo.organization.member_id,
            SubDomain: getSubdomainFromRestUrl(userInfo.rest.rest_instance_url),
        });
        clientId.value = "";
        clientSecret.value = "";
        notifications.value.push({
            id: `${Date.now()}`,
            title: "Success",
            subtitle: "Credentials saved successfully.",
        });
    } catch (err) {
        loading.value = false;
        throw new Error(
            "An internal error occurred while trying to save the credentials in Laasie. Please try again later."
        );
    }

    loading.value = false;
}

function onNotificationClose(id: string) {
    const index = notifications.value.findIndex((n) => n.id === id);
    notifications.value.splice(index, 1);
}
</script>

<script lang="ts">
export default {
    data: function () {
        return {
            showSuccess: false,
            showError: false,
            isValid: false,
        };
    },
};
</script>
<style lang="scss" scoped>
.slds-form {
    display: flex;
    flex-flow: column nowrap;
    align-items: center;

    .slds-form-element {
        max-width: 20%;
    }

    .slds-button {
        width: 20%;
    }
}
</style>
