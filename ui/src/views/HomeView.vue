<template>
    <LoadingSpinner v-if="loading"></LoadingSpinner>
    <header class="slds-global-header_container">
        <div class="slds-global-header slds-grid slds-grid_align-end">
            <div class="slds-global-header__item slds-size_5-of-6">
                <span class="slds-text-heading_small">Laasie Onboarding</span>
            </div>
            <div class="slds-global-header__item slds-size_1-of-6"></div>
        </div>
    </header>
    <main style="margin-top: 4rem">
        <RouterView />
    </main>
</template>
<script setup lang="ts">
import { onMounted, ref } from "vue";
import { RouterView } from "vue-router";

import LoadingSpinner from "@/components/LoadingSpinner.vue";

import Cookies from "js-cookie";

import { initLaasieApiAccessToken } from "@/externalApiClient";

const loading = ref(false);
const csrfToken = ref<string>();

onMounted(async () => {
    await initLaasieApiAccessToken();
    csrfToken.value = Cookies.get("X-CSRF-Token");
});
</script>
