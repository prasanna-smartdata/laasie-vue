<template>
     <div class="slds-path slds-m-top_medium slds-m-bottom_medium  slds-m-left_medium  slds-m-right_medium">
            <div class="slds-grid slds-path__track">
                <div class="slds-grid slds-path__scroller-container">
                    <div class="slds-path__scroller">
                        <div class="slds-path__scroller_inner">
                            <ul
                                class="slds-path__nav"
                                role="listbox"
                                aria-orientation="horizontal"
                            >
                                <li
                                    class="slds-path__item btn-slds-is-current slds-is-active slds-is-incomplete"
                                    role="presentation"
                                >
                                    <a
                                        aria-selected="true"
                                        class="slds-path__link"
                                        id="path-1"
                                        role="option"
                                    >
                                        <span class="slds-path__stage">
                                            <UtilityIcon
                                                svgClass="slds-icon slds-icon_x-small"
                                                iconName="check"
                                            />
                                            <span class="slds-assistive-text">
                                                Current Stage:
                                            </span>
                                        </span>
                                        <span class="slds-path__title">
                                            S2S Application Setup
                                        </span>
                                    </a>
                                </li>

                                <li
                                class="slds-path__item btn-slds-is-current slds-is-inactive slds-is-incomplete"
                                    role="presentation"
                                >
                                    <a
                                        aria-selected="false"
                                        class="slds-path__link"
                                        id="path-3"
                                        role="option"
                                    >
                                        <span class="slds-path__stage">
                                            <UtilityIcon
                                                svgClass="slds-icon slds-icon_x-small"
                                                iconName="check"
                                            />
                                        </span>
                                        <span class="slds-path__title">
                                            Review Setup
                                        </span>
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
   
  </template>
  
  <script setup lang="ts">
  import { useRouter } from 'vue-router';

    const router = useRouter();
    let currentPathObject = router.currentRoute.value;
    
  </script>
  
  <style>
  
  </style>