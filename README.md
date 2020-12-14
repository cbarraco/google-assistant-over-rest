# google-assistant-over-rest
Contact Google Assistant over a very simple REST API

![Docker Automated build](https://img.shields.io/docker/automated/cbarraco/google-assistant-over-rest)

This is a Docker container that contains a web server capable of talking to Google Assistant. You can simply make an HTTP POST to `/command` containing a command written as a normal sentence. This normal sentence is what you would say to Google Assistant to execute a command, like: "Turn on the kitchen lights"

## How to run:

```
docker run 
    -e DEVICE_MODEL_ID="<YOUR_DEVICE_MODEL_ID>"
    -e DEVICE_ID="<YOUR_DEVICE_ID>"
    -p 5000:5000
    -v <SOME_PATH_ON_YOUR_SYSTEM>/credentials.json:/usr/src/app/credentials.json
    cbarraco/google-assistant-over-rest
```
