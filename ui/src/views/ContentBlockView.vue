<template>Coming Soon!</template>
<script lang="ts" setup>
import type SDK from "blocksdk";
import { inject, onMounted } from "vue";

const blockSdk = inject<SDK>("blockSdk");

onMounted(() => {
    blockSdk?.getData((_data) => {
        setTimeout(async () => {
            // TODO: If there is user data saved in the block,
            // use that data to update the view accordingly.
        }, 0);
    });
});
</script>
