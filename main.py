# Copyright (C) 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
import json
import sys

import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)

from bs4 import BeautifulSoup

from flask import Flask
from flask import request

app = Flask(__name__)


ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5


class RestAssistant(object):
    """REST API Assistant that supports basic commands.

    Args:
      language_code: language for the conversation.
      device_model_id: identifier of the device model.
      device_id: identifier of the registered device instance.
      channel: authorized gRPC channel for connection to the
        Google Assistant API.
    """

    def __init__(self, language_code, device_model_id, device_id, channel):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_state = None
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(channel)

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False

    def assist(self, text_query):
        """Send a text request to the Assistant.
        """
        def iter_assist_requests():
            config = embedded_assistant_pb2.AssistConfig(
                audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                    encoding='LINEAR16',
                    sample_rate_hertz=16000,
                    volume_percentage=0,
                ),
                dialog_state_in=embedded_assistant_pb2.DialogStateIn(
                    language_code=self.language_code,
                    conversation_state=self.conversation_state,
                    is_new_conversation=True,
                ),
                device_config=embedded_assistant_pb2.DeviceConfig(
                    device_id=self.device_id,
                    device_model_id=self.device_model_id,
                ),
                text_query=text_query,
            )
            req = embedded_assistant_pb2.AssistRequest(config=config)
            yield req

        text_response = None
        for resp in self.assistant.Assist(iter_assist_requests(), DEFAULT_GRPC_DEADLINE):
            if resp.screen_out.data:
                soup = BeautifulSoup(resp.screen_out.data, 'html.parser')
                text_response = soup.get_text()
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                self.conversation_state = conversation_state
            if resp.dialog_state_out.supplemental_display_text:
                text_response = resp.dialog_state_out.supplemental_display_text
        return text_response


logging.basicConfig(level=logging.DEBUG)

try:
    # with open('/usr/src/app/credentials.json', 'r') as f:
    with open('credentials.json', 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None, **json.load(f))
        http_request = google.auth.transport.requests.Request()
        credentials.refresh(http_request)
except Exception as e:
    logging.error('Error loading credentials: %s', e)
    sys.exit()

grpc_channel = google.auth.transport.grpc.secure_authorized_channel(credentials, http_request, ASSISTANT_API_ENDPOINT)
logging.info('Connecting to %s', ASSISTANT_API_ENDPOINT)

device_model_id = os.environ.get('DEVICE_MODEL_ID')
device_id = os.environ.get('DEVICE_ID')
language_code = os.environ.get('LANGUAGE_CODE')
if language_code == None:
    language_code = 'en-US'

assistant = RestAssistant(language_code, device_model_id, device_id, grpc_channel)

@app.route('/command', methods=['POST'])
def command_api():
    logging.info('Received method call: %s', request.json)
    command = request.json["command"]
    logging.info('Received command: %s', command)
    reply = assistant.assist(text_query=command)
    if reply == None:
        return ""
    response = {
        "result": reply
    }
    return json.dumps(response)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
