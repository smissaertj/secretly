# Secretly
## Developers Institute - Hackathon #2
A VueJS / Flask web application to send password protected messages to a 3rd party.

[![Netlify Status](https://api.netlify.com/api/v1/badges/038c1a83-f4b5-4b9d-9bb0-20ebc3f1e654/deploy-status)](https://app.netlify.com/sites/cool-as-code-secretly/deploys)  
Demo: https://secretly.joeri.xyz/

*Usage Instructions:*
- Register an account, use a working email address.
- Activate the account by clicking the activation link in the email.
- Login to send a message: Use a valid email for the destination.
- Click "profile" to see sent messages.



# secretly-client
The Secretly frontend, built with VueJS/Vite and TailwindCSS.

Features:
- Computed Properties
- Class and Style bindings
- Conditional rendering
- Pinia State Management
- Event handling
- Lifecycle hooks


### Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

# secretly-api
The Secretly backend, a REST API built with Python & the Flask framework.

### Project Setup

```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r secretly-api/requirements.txt
```

### Run Development Server

```sh
python3 secretly-api/app.py
```

### Or using Podman (or Docker)
```shell
cd secretly-api
podman build -f Dockerfile
podman run --name secretely-api -p 8080:8080 <image_name>
```
