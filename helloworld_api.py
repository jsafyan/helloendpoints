"""Hello World API implemented using Google Cloud Endpoints.

Defined here as the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

"""Used by ProtoRPC when creating names for ProtoRPC messages. Will show up 
as a prefix to message class names in the discovery doc and client libs.
"""

package = 'Hello'

class Greeting(messages.Message):
	"""Greeting that stores a message."""
	message = messages.StringField(1)

class GreetingCollection(messages.Message):
	"""Collection of Greetings."""
	items = messages.MessageField(Greeting, 1, repeated=True)

STORED_GREETINGS = GreetingCollection(items=[
	Greeting(message='hello, world!'),
	Greeting(message='goodbye, world!')
])