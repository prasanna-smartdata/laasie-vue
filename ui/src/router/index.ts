import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import OnboardingView from "@/views/ApplicationSetupView.vue";
import ContentBlockView from "@/views/ContentBlockView.vue";

/**
 * Throws an error if the app is loaded outside of SFMC
 * when it is not running on a localhost domain.
 * However, allows the auth completion route to be loaded.
 */
function assertSfmcParent() {
    if (
        window.self === window.top &&
        !window.location.hostname.endsWith("localhost")
    ) {
        throw new Error(
            "This application is for use in Salesforce Marketing Cloud only."
        );
    }
}

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    // IMPORTANT: If a component tied to a route accepts props as inputs
    // then make sure the path parameter of the route uses the same prop
    // name.
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeView,
            beforeEnter: assertSfmcParent,
            children: [
                {
                    path: "",
                    name: "onboarding",
                    component: OnboardingView,
                },
                {
                    path: "contentblock",
                    name: "contentblock",
                    component: ContentBlockView,
                },
            ],
        },
    ],
});

export default router;
