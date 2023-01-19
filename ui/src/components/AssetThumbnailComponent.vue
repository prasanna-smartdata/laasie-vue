<template>
    <LoadingSpinner
        v-if="loading"
        :size="'slds-spinner_x-small'"
    ></LoadingSpinner>
    <img v-if="thumbnailBase64" :src="thumbnailBase64" />
</template>
<script setup lang="ts">
import { getThumbnailBase64 } from "@/sfmcClient";
import { onMounted, ref } from "vue";

import LoadingSpinner from "./LoadingSpinner.vue";

interface Props {
    urlPath: string;
}

const props = defineProps<Props>();
const thumbnailBase64 = ref();
const loading = ref(false);

onMounted(async () => {
    loading.value = true;
    thumbnailBase64.value = await getThumbnailBase64(props.urlPath);
    loading.value = false;
});
</script>
