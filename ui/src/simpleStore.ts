import { ref } from "vue";

export interface SimpleStore {
    defaultCategoryId?: number;
}

const simpleState: SimpleStore = {};

export const store = ref<SimpleStore>(simpleState);
