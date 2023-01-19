<template>
    <div
        v-if="actions && actions.length"
        :class="[
            'slds-dropdown-trigger',
            'slds-dropdown-trigger_click',
            { 'slds-is-open': showActionsMenu },
        ]"
    >
        <button
            v-if="!avatarMenu"
            class="slds-button slds-button_icon slds-button_icon-border-filled slds-button_icon-x-small"
            aria-haspopup="true"
            :aria-expanded="showActionsMenu"
            title="Show More"
            @click="showActionsMenu = !showActionsMenu"
        >
            <UtilityIconComponent
                svg-class="slds-button__icon"
                icon-name="down"
            ></UtilityIconComponent>
            <span class="slds-assistive-text">Show More</span>
        </button>
        <button
            v-else
            class="slds-button slds-button_icon slds-global-actions__avatar slds-global-actions__item-action"
            aria-haspopup="true"
            :aria-expanded="showActionsMenu"
            @click="showActionsMenu = !showActionsMenu"
        >
            <span class="slds-avatar slds-avatar_circle slds-avatar_medium">
                <span class="slds-icon_container slds-icon-standard-user">
                    <ActionIconComponent
                        svg-class="slds-icon"
                        icon-name="user"
                    ></ActionIconComponent>
                </span>
            </span>
        </button>
        <div
            v-if="showActionsMenu"
            class="slds-dropdown slds-dropdown_actions slds-dropdown_right"
        >
            <ul class="slds-dropdown__list" role="menu">
                <MenuItemComponent
                    :actions="actions"
                    @action="actionClicked"
                ></MenuItemComponent>
            </ul>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref } from "vue";

import UtilityIconComponent from "./icons/UtilityIconComponent.vue";
import MenuItemComponent, { type Action } from "./MenuItemComponent.vue";
import ActionIconComponent from "./icons/ActionIconComponent.vue";

interface Props {
    actions?: Action[];
    avatarMenu?: boolean;
}

defineProps<Props>();

const emit = defineEmits<{ (e: "action", action: Action): void }>();

const showActionsMenu = ref(false);

function actionClicked(item: Action) {
    emit("action", item);
    showActionsMenu.value = !showActionsMenu.value;
}
</script>
