<template>
    <div
        role="status"
        :class="[
            'slds-spinner',
            size ?? 'slds-spinner_small',
            { 'slds-spinner_brand': brand },
        ]"
    >
        <span class="slds-assistive-text">Loading</span>
        <div class="slds-spinner__dot-a"></div>
        <div class="slds-spinner__dot-b"></div>
    </div>
</template>
<script setup lang="ts">
type SpinnerSize =
    | "slds-spinner_x-small"
    | "slds-spinner_small"
    | "slds-spinner_medium"
    | "slds-spinner_large";

interface Props {
    size?: SpinnerSize;
    brand?: boolean;
}

defineProps<Props>();
</script>
