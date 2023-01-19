<template>
    <div class="slds-notification-container">
        <section
            v-for="(notif, index) in props.notifications"
            :key="index"
            class="slds-notification"
            role="dialog"
            :aria-labelledby="notif.id"
            :aria-describedby="`dialog-body-${notif.id}`"
        >
            <div
                class="slds-notification__body"
                :id="`dialog-body-${notif.id}`"
            >
                <a class="slds-notification__target slds-media" href="#">
                    <div class="slds-media__body">
                        <h2
                            class="slds-text-heading_small slds-m-bottom_xx-small"
                            :id="notif.id"
                        >
                            <span class="slds-assistive-text"
                                >task notification:</span
                            >{{ notif.title }}
                        </h2>
                        <p>{{ notif.subtitle }}</p>
                    </div>
                </a>
                <button
                    class="slds-button slds-button_icon slds-button_icon-container slds-notification__close"
                    :title="notif.title"
                    @click="$emit('onNotificationClose', notif.id)"
                >
                    <UtilityIconComponent
                        svg-class="slds-button__icon"
                        icon-name="close"
                    ></UtilityIconComponent>
                    <span class="slds-assistive-text"
                        >Dismiss {{ notif.title }} notification</span
                    >
                </button>
            </div>
        </section>
    </div>
</template>
<script lang="ts" setup>
import UtilityIconComponent from "./icons/UtilityIconComponent.vue";

export interface NotificationContent {
    id: string;
    title: string;
    subtitle: string;
}

interface Props {
    notifications: NotificationContent[];
}

const props = defineProps<Props>();

defineEmits<{
    (event: "onNotificationClose", id: string): void;
}>();
</script>
