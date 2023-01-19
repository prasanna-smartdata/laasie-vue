import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
    server: {
        port: 3000,
        https: {
            cert: "../api/localhost.crt",
            key: "../api/localhost.key",
        },
        proxy: {
            "/oauth2": {
                target: "https://app.localhost",
                // changeOrigin: true,
                secure: false,
            },
            "/api": {
                target: "https://app.localhost",
                // changeOrigin: true,
                secure: false,
            },
            "/auth": {
                target: "https://app.localhost",
                // changeOrigin: true,
                secure: false,
            },
        },
    },
    base: "/ui/",
    build: {
        outDir: "../api/ui",
        emptyOutDir: true,
    },
});
