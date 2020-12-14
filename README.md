# google-assistant-over-rest
Contact Google Assistant over a very simple REST API

![Docker Automated build](https://img.shields.io/docker/automated/cbarraco/google-assistant-over-rest)

This is a Docker container that contains a web server capable of talking to Google Assistant. You can simply make an HTTP POST to `/command` containing a command written as a normal sentence. This normal sentence is what you would say to Google Assistant to execute a command, like: "Turn on the kitchen lights". The API will return a response which is the text version of what the Google Assistant would say.

## How to use

### Request
HTTP POST to `http://localhost:5000/command` with JSON request body `{"command": "what time is it?"}`

### Response
Response with JSON body `{"result": "It's 10:54 a.m."}`

## How to run:

```
docker run 
    -e DEVICE_MODEL_ID="<YOUR_DEVICE_MODEL_ID>"
    -e DEVICE_ID="<YOUR_DEVICE_ID>"
    -p 5000:5000
    -v <SOME_PATH_ON_YOUR_SYSTEM>/credentials.json:/usr/src/app/credentials.json
    cbarraco/google-assistant-over-rest
```
In order to get the above fields, you need to create a new project on https://console.actions.google.com/ using the "Other" project type. Once the project is created, you can request a credentials.json file using the google-oauth-tool and your client secret.
