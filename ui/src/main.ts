import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import blockSdkPlugin from "@/plugins/sfmcBlockSdk.plugin";

import "@salesforce-ux/design-system/scss/index.scss";

const app = createApp(App);

app.use(router);
app.use(blockSdkPlugin);

app.mount("#app");
