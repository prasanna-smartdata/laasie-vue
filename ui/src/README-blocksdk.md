# README for SFMC blocksdk

The [`blocksdk`](https://github.com/salesforce-marketingcloud/blocksdk) is SFMC's SDK for interacting with the SFMC Content Builder editor framework.
It allows us to set the HTML content in a block, save and retrieve any data specific to the block.

The SDK is an important piece for SFMC custom content block. It is what allows us to inject HTML into the block that a user is editing.

See the official tutorial for developing a custom content block: https://developer.salesforce.com/docs/marketing/marketing-cloud/guide/develop-block-widget.html

## getData/setData

The pair of methods used to get/set data related to a specific instance of a content block. The type of data that can be saved is any serializable JS object.
Note that because we use TypeScript, to give these methods some type-safety, TypeScript's [interface merging feature](https://www.typescriptlang.org/docs/handbook/declaration-merging.html#merging-interfaces) was used. See `src/app.d.ts`.

## TypeScript

It does not come with its own TypeScript types so a [PR](https://github.com/salesforce-marketingcloud/blocksdk/pull/13) was opened in the repo but at the time of this writing, there is no sign of that being merged. So a copy of the definition file exists in this repo as well. See `src/blocksdk.d.ts`.
