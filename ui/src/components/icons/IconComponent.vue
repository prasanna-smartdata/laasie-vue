<template>
    <svg :class="svgClass" aria-hidden="true">
        <use :xlink:href="`${svgUrl}#${iconName}`"></use>
    </svg>
</template>
<script setup lang="ts">
import svgUrl from "@salesforce-ux/design-system/assets/icons/standard-sprite/svg/symbols.svg";

interface Props {
    iconName: string;
    svgClass: string;
}

defineProps<Props>();
</script>
