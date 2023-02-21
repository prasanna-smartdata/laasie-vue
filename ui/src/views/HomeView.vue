<template>
    <div class="slds-theme_default"  style=" height: 650px" >
        <LoadingSpinner v-if="loading"></LoadingSpinner>

        <div className=" slds-text-heading_medium slds-m-left_small slds-m-top_xx-small">
            
            Configuration Pages
        </div>

        <div
            class="slds-box slds-m-top--large slds-m-left_small slds-m-right_small">
            <div class="slds-m-top--xxx-large">
                <Header></Header>
            </div>
        </div>
        <div
            class="slds-m-around_small slds-border_bottom slds-border_top slds-border_left slds-border_right"
        >
            <RouterView />
        </div>
    </div>
</template>
<script setup lang="ts">
import { onMounted, onUpdated, ref } from "vue";
import { RouterView, useRouter } from "vue-router";

import LoadingSpinner from "@/components/LoadingSpinner.vue";
import Header from "@/components/HeaderComponent.vue";

import Cookies from "js-cookie";

import { initLaasieApiAccessToken } from "@/externalApiClient";
import { getUserInfo } from "@/sfmcClient";

const loading = ref(false);
const csrfToken = ref<string>();
onMounted(async () => {
    // await initLaasieApiAccessToken();
    csrfToken.value = Cookies.get("X-CSRF-Token");
    try {
    const userInfo = await getUserInfo();
        console.log(userInfo);
    } catch (error) {
        console.log(error);
    }
});

onUpdated(async ()=>{
   
})
</script>
