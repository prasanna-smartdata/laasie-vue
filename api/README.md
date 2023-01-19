# Flask-based API

This folder contains a REST API implemented in Python using the [Flask](https://flask.palletsprojects.com/en/2.1.x/) web framework.

The main purpose of this app is to serve as the redirect callback for Oauth

## Development

If you use VS Code, make sure you have the Python language extensions installed. If not, VS Code usually
would prompt you to install them as soon as you open a file from this folder.

To start the Flask server locally, simply run `make run_api` from the root of this repo where the `Makefile`
exists. By default, it supports hot-reloading.

**Note**: See the `.env` section below about the required environment variables.

### Static File Server

This Flask-based service also acts as a static file server. The Vue app's `vite.config.ts` is configured
to output the UI bundles to a folder called `ui` under this folder. The `ui` folder under the `api` folder
is ignored by git (see `.gitignore`.)

When you are testing locally you won't be able to use hot-reload functionality of the Vue app. So you have to
run `make build` every time you make a change to the UI so that the static file server can serve the updated
UI assets in the `<iframe>` on SFMC on page refresh. It works because SFMC is hitting your ngrok tunnel which
proxies to your `localhost:5000` which then serves whatever files are on disk on your machine.

### Testing

Use ngrok to expose your `localhost` service at port `5000` to the internet so that you can test your local changes
in SFMC using an Installed Package whose redirect URI and content block URL are your ngrok tunnel address.

### `.env`

For local development, you could either set the environment variables in your shell profile so that the
service can read them or create an `.env` file in this (`/api`) folder with the required variables.

As of this writing, the following are the required values. See `env_config.py` for the most current set of required variables.

```
JWT_SECRET=<set a random value>
SECRET_KEY=<set a random value>
SELF_DOMAIN=https://app.localhost
REDIRECT_UI_TO_LOCALHOST=true
SFMC_OAUTH2_CALLBACK_PATH=/callback
SFMC_CLIENT_ID=
SFMC_CLIENT_SECRET=
# The tenant subdomain for the customer's SFMC PBO account.
# Change this if the account you are using is not the same.
# You can verify if it's the same by comparing this with the value of the
# auth endpoint in the Installed Package app you are using for local
# development.
SFMC_DEFAULT_TENANT_SUBDOMAIN=

# Either register an API application in the customer's developer portal
# to get a client ID/secret or ask the customer to register one and give
# them to you. The registered app should be of type Web App if multiple
# client types are possible.
#
# For local development, the redirect URI should be set to
# https://app.localhost/oauth2/{customer_name}/callback.
EXTERNAL_API_CLIENT_ID=
EXTERNAL_API_CLIENT_SECRET=
```

## Blueprints

Organize the REST API surface using Flask [Blueprints](https://flask.palletsprojects.com/en/2.1.x/tutorial/views/).

## Linting

Linting is done using `mypy` and the formatter is `black`. VS Code will once again prompt to install those
if they are not already as they are listed in this project's settings file under the `.vscode` folder.
