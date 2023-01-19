<template>
    <li
        v-for="(item, index) in actions"
        :key="index"
        :class="[
            'slds-dropdown__item',
            { 'slds-has-submenu': item.hasSubmenu },
        ]"
        role="presentation"
        @click="actionClicked(item)"
    >
        <a
            href="#"
            role="menuitem"
            :tabindex="index"
            :aria-haspopup="item.hasSubmenu"
            :aria-expanded="submenuExpanded"
        >
            <span class="slds-truncate" :title="item.name">{{
                item.name
            }}</span>
            <UtilityIconComponent
                v-if="item.hasSubmenu"
                svg-class="slds-icon slds-icon_x-small slds-icon-text-default slds-m-left_small slds-shrink-none"
                icon-name="right"
            ></UtilityIconComponent>
        </a>
        <div
            v-if="item.hasSubmenu"
            class="slds-dropdown slds-dropdown_submenu slds-dropdown_submenu-left"
            style="width: 150px"
        >
            <ul
                class="slds-dropdown__list"
                style="overflow-y: auto; max-height: 200px"
                role="menu"
            >
                <MenuItemComponent
                    :actions="item.submenu"
                    @action="actionClicked"
                ></MenuItemComponent>
            </ul>
        </div>
    </li>
</template>
<script lang="ts">
export interface Action {
    /**
     * The unique id of the action that was selected by the user.
     */
    id: string;
    /**
     * The display name of the action.
     */
    name: string;
    /**
     * The index of the item that the action was invoked on.
     * Use this value to retrieve the corresponding item
     * from the list of options that this action was generated
     * from.
     */
    index: number;
    value?: string;
    hasSubmenu?: boolean;
    submenu?: Action[];
    parentMenuItemId?: string;
}
</script>
<script setup lang="ts">
import { ref } from "vue";

import UtilityIconComponent from "./icons/UtilityIconComponent.vue";

interface Props {
    actions?: Action[];
}

defineProps<Props>();

const emit = defineEmits<{ (e: "action", action: Action): void }>();

const submenuExpanded = ref(false);

function actionClicked(item: Action) {
    // If an item with a submenu is clicked, then toggle
    // the submenu.
    if (item.hasSubmenu) {
        submenuExpanded.value = !submenuExpanded.value;
        return;
    }

    // Otherwise, emit an action event and toggle the actions menu.
    emit("action", item);
}
</script>
