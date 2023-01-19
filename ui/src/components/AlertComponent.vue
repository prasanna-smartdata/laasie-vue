<template>
    <div
        :class="['slds-notify', 'slds-notify_alert', `slds-alert_${kind}`]"
        role="alert"
        style="z-index: 9999"
    >
        <span class="slds-assistive-text">{{ kind }}</span>
        <span
            :class="[
                'slds-icon_container',
                `slds-icon-utility-${kind}`,
                'slds-m-right_x-small',
            ]"
            title="alert icon"
        >
            <UtilityIconComponent
                svg-class="slds-icon slds-icon_x-small"
                :icon-name="kind"
            ></UtilityIconComponent>
        </span>
        <h2>
            {{ message }}
            <router-link v-if="link" :to="link.href">{{
                link.label
            }}</router-link>
        </h2>
        <div class="slds-notify__close">
            <button
                class="slds-button slds-button_icon slds-button_icon-small slds-button_icon-inverse"
                title="Close"
                @click="$emit('close', id)"
            >
                <UtilityIconComponent
                    svg-class="slds-button__icon"
                    icon-name="close"
                ></UtilityIconComponent>
                <span class="slds-assistive-text">Close</span>
            </button>
        </div>
    </div>
</template>
<script lang="ts">
export interface Link {
    href: string;
    label: string;
}

export interface AlertProps {
    id: number;
    kind: "error" | "warning" | "info";
    message: string;
    link?: Link;
}
</script>
<script setup lang="ts">
import UtilityIconComponent from "@/components/icons/UtilityIconComponent.vue";

defineProps<AlertProps>();

defineEmits<{ (e: "close", id: number): void }>();
</script>
