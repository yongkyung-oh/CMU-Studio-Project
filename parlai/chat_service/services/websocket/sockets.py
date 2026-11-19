#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Dict, TypeVar
from parlai.chat_service.utils.local import local_authority, local_origin
from tornado.websocket import WebSocketHandler
import uuid
import logging
import json


def get_rand_id():
    return str(uuid.uuid4())


T = TypeVar('T', bound='MessageSocketHandler')


class MessageSocketHandler(WebSocketHandler):
    def __init__(self: T, *args, **kwargs):
        self.subs: Dict[int, T] = kwargs.pop('subs')

        def _default_callback(message, socketID):
            logging.warn(f"No callback defined for new WebSocket messages.")

        self.message_callback = kwargs.pop('message_callback', _default_callback)
        self.sid = get_rand_id()
        super().__init__(*args, **kwargs)

    def prepare(self):
        if not local_authority(self.request.host, self.request.connection.stream.socket.getsockname()[1]):
            from tornado.web import HTTPError
            raise HTTPError(403)

    def open(self):
        """
        Opens a websocket and assigns a random UUID that is stored in the class-level
        `subs` variable.
        """
        if self.sid not in self.subs.values():
            self.subs[self.sid] = self
            logging.info(f"Opened new socket from ip: {self.request.remote_ip}")
            logging.info(f"Current subscribers: {self.subs}")

    def on_close(self):
        """
        Runs when a socket is closed.
        """
        self.subs.pop(self.sid, None)

    def on_message(self, message_text):
        """
        Callback that runs when a new message is received from a client See the
        chat_service README for the resultant message structure.

        Args:
            message_text: A stringified JSON object with a text or attachment key.
                `text` should contain a string message and `attachment` is a dict.
                See `WebsocketAgent.put_data` for more information about the
                attachment dict structure.
        """
        logging.info('websocket message from client: {}'.format(message_text))
        try:
            message = json.loads(message_text)
            if not isinstance(message, dict) or not isinstance(message.get('text', ''), str):
                raise ValueError
        except (ValueError, TypeError):
            self.close(1007, 'Expected a JSON object with text')
            return
        message = {
            'text': message.get('text', ''),
            'payload': message.get('payload'),
            'sender': {'id': self.sid},
            'recipient': {'id': 0},
        }
        self.message_callback(message)

    def check_origin(self, origin):
        return local_origin(origin, self.request.connection.stream.socket.getsockname()[1])
