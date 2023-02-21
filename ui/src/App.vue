<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";
import { RouterView } from "vue-router";

import { refreshSfmcToken, settings as sfmcSettings } from "./sfmcClient";
import { setSessionStartTime } from "./tokenUtils";
import AlertComponent, {
    type AlertProps,
} from "./components/AlertComponent.vue";

const alerts = ref<AlertProps[]>([]);

function addAlert(message: string) {
    const id = Date.now();
    alerts.value.push({
        id,
        kind: "error",
        message,
    });
    setTimeout(() => closeAlert(id), 10000);
}

function onUnhandledRejection(e: PromiseRejectionEvent) {
    console.error(
        "caught an unhandled promise rejection from the app",
        e.reason
    );
    addAlert(e.reason.toString());
}

function onError(e: ErrorEvent) {
    console.error("An unhandled error was encountered", e);
    addAlert(
        "An unexpected error occurred. Please report this error to your system administrator."
    );
}

onMounted(async () => {
    window.addEventListener("unhandledrejection", onUnhandledRejection);
    window.addEventListener("error", onError);

    if (document.cookie.includes(sfmcSettings.accessTokenCookieName)) {
        setTimeout(refreshSfmcToken, sfmcSettings.tokenRefreshInterval);
    } else {
        await refreshSfmcToken();
    }

    setSessionStartTime();
});

onBeforeUnmount(() => {
    window.removeEventListener("unhandledrejection", onUnhandledRejection);
});

function closeAlert(id: number) {
    const index = alerts.value.findIndex((a) => a.id === id);
    alerts.value.splice(index, 1);
}
</script>

<template>
    <div>
        <RouterView />
    </div>
    <AlertComponent
        v-for="(alert, index) in alerts"
        :id="alert.id"
        :message="alert.message"
        :kind="alert.kind"
        :key="index"
        @close="closeAlert"
    ></AlertComponent>
</template>
<style>
  @import url('../node_modules/@salesforce-ux/design-system/assets/styles/salesforce-lightning-design-system.min.css');

  html {
    height: 100%;
}
body {
    height: 100%;
}
#app {
    height: 100%;
}
#app > form {
    max-width: 100%;
  }

  

</style>