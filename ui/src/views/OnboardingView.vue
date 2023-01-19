<template>
    <LoadingSpinner v-if="loading" />
    <div class="slds-form sfmc">
        <p class="slds-var-p-bottom_medium">
            Please enter the client ID and secret for a server-to-server
            Installed Package registered in your business unit.
        </p>
        <div class="slds-form-element slds-form-element_horizontal">
            <label class="slds-form-element__label" for="client-id"
                >Client ID<abbr
                    class="slds-required"
                    title="(required) The client ID of the server-to-server installed package"
                    >*</abbr
                ></label
            >
            <div class="slds-form-element__control">
                <input
                    type="text"
                    id="client-id"
                    placeholder="Client ID"
                    class="slds-input"
                    v-model.trim="clientId"
                />
            </div>
        </div>
        <div class="slds-form-element slds-form-element_horizontal">
            <label class="slds-form-element__label" for="client-secret"
                >Client Secret<abbr
                    class="slds-required"
                    title="(required) The client secret of the server-to-server installed package"
                    >*</abbr
                ></label
            >
            <div class="slds-form-element__control">
                <input
                    type="password"
                    id="client-secret"
                    placeholder="Client Secret"
                    class="slds-input"
                    v-model.trim="clientSecret"
                />
            </div>
        </div>
        <button
            class="slds-button slds-button_brand"
            @click="onSubmitClick"
            :disabled="!clientId || !clientSecret || loading"
        >
            Submit
        </button>
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
