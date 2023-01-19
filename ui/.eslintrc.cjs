/* eslint-env node */
require("@rushstack/eslint-patch/modern-module-resolution");

module.exports = {
    root: true,
    extends: [
        "plugin:vue/vue3-essential",
        "eslint:recommended",
        "@vue/eslint-config-typescript/recommended",
    ],
    rules: {
        "@typescript-eslint/no-explicit-any": "off",
        "@typescript-eslint/no-unused-vars": [
            "warn",
            { varsIgnorePattern: "^_", argsIgnorePattern: "^_" },
        ],
    },
    env: {
        "vue/setup-compiler-macros": true,
    },
};
