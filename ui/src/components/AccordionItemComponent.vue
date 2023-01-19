<template>
    <li class="slds-accordion__list-item">
        <section
            :class="['slds-accordion__section', { 'slds-is-open': expanded }]"
        >
            <div class="slds-accordion__summary">
                <h2 class="slds-accordion__summary-heading">
                    <button
                        class="slds-button slds-button_reset slds-accordion__summary-action"
                        :aria-controls="id"
                        :aria-expanded="expanded"
                        :title="title"
                        @click="expanded = !expanded"
                    >
                        <UtilityIconComponent
                            svg-class="slds-accordion__summary-action-icon slds-button__icon slds-button__icon_left"
                            icon-name="switch"
                        ></UtilityIconComponent>
                        <span class="slds-accordion__summary-content">{{
                            title
                        }}</span>
                    </button>
                </h2>
                <MenuComponent
                    v-if="actions"
                    :actions="actions"
                    @action="$emit('action', $event)"
                ></MenuComponent>
            </div>
            <div :hidden="!expanded" class="slds-accordion__content" :id="id">
                <div v-if="content">{{ content }}</div>
                <slot></slot>
            </div>
        </section>
    </li>
</template>
<script setup lang="ts">
import { ref } from "vue";

import UtilityIconComponent from "./icons/UtilityIconComponent.vue";
import MenuComponent from "@/components/MenuComponent.vue";
import type { Action } from "@/components/MenuItemComponent.vue";

interface Props {
    id: string;
    title: string;
    content?: string;
    actions?: Action[];
}

defineProps<Props>();

defineEmits<{ (e: "action", action: Action): void }>();

const expanded = ref(false);
</script>
