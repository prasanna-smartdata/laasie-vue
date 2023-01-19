<template>
    <div class="slds-form-element">
        <label v-if="showLabel" class="slds-form-element__label" :for="id">
            <abbr class="slds-required" title="required">* </abbr
            >{{ label }}</label
        >
        <div class="slds-form-element__control">
            <div class="slds-select_container">
                <select
                    class="slds-select"
                    :id="id"
                    @change="onMenuItemSelected"
                    :value="selectedValue"
                >
                    <option
                        v-for="(item, index) in items"
                        :key="index"
                        :value="item.value"
                    >
                        {{ item.name }}
                    </option>
                </select>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref } from "vue";

export interface MenuItem {
    name: string;
    value: string;
}

interface Props {
    items: MenuItem[];
    id: string;
    label?: string;
    showLabel: boolean;
    selectedValue: string;
}
const selectedItem = ref<MenuItem>();

const props = defineProps<Props>();

const emit = defineEmits<{ (e: "selectionChanged", item: MenuItem): void }>();

function onMenuItemSelected(event: Event) {
    const value = (event.target as HTMLSelectElement).value;
    const item = props.items.filter((i) => i.value === value)[0];
    selectedItem.value = item;
    emit("selectionChanged", item);
}
</script>
