<template>
    <article class="slds-card">
        <div class="slds-card__header slds-grid">
            <header
                class="slds-media slds-media_center slds-has-flexi-truncate"
            >
                <div class="slds-media__figure">
                    <span
                        class="slds-icon_container slds-icon-standard-task"
                        title="task"
                    >
                        <slot name="icon"></slot>
                        <span class="slds-assistive-text">task</span>
                    </span>
                </div>
                <div class="slds-media__body">
                    <h2 class="slds-card__header-title">
                        <router-link
                            v-if="!!href"
                            :title="title"
                            class="slds-card__header-link slds-truncate"
                            :to="href"
                        >
                            <span>{{ title }}</span>
                        </router-link>
                        <span v-else>{{ title }}</span>
                    </h2>
                </div>
            </header>
        </div>
        <div class="slds-card__body slds-card__body_inner">
            <slot name="body"></slot>
        </div>
    </article>
</template>
<script setup lang="ts">
import type { PropType } from "vue";
import type { RouteLocationRaw } from "vue-router";

defineProps({
    title: {
        type: String,
        required: true,
    },
    href: {
        type: Object as PropType<RouteLocationRaw>,
        required: false,
    },
});
</script>
