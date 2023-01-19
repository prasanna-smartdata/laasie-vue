import type { App } from "vue";

import SDK from "blocksdk";

export default {
    install: (app: App) => {
        // https://github.com/salesforce-marketingcloud/blocksdk#initialization-options
        const blockSdk = new SDK({
            tabs: [
                "htmlblock",
                "stylingblock",
            ],
        });

        app.provide("blockSdk", blockSdk);
    },
};
