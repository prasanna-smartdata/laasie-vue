import type { Data } from "blocksdk";

declare module "blocksdk" {
    // Use TS interface merging to add properties to the Data interface.
    // This allows us to use the `getData`/`setData` methods of the blocksdk
    // and have the data parameter be strongly-typed with these custom
    // properties.
    // Note: Do not modify the types of the existing properties.
    // These properties are stored as user data in each user's
    // custom content block. It is safe to add new properties.
    // If you want to "change" a property's type, you should
    // add a new one and deprecate the old property name by
    // not using it in your `setData` calls.
    //
    // interface Data {
    // }
}
