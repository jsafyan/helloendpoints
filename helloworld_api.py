"""Hello World API implemented using Google Cloud Endpoints.

Defined here as the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


WEB_CLIENT_ID = 'replace with web client app id'
ANDROID_CLIENT_ID = 'replace with Android client id'
IOS_CLIENT_ID = 'replace with iOS client id'
ANDROID_AUDIENCE = WEB_CLIENT_ID

#Used by ProtoRPC when creating names for ProtoRPC messages. Will show up 
#as a prefix to message class names in the discovery doc and client libs.
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

@endpoints.api(name='helloworld', version='v1',
	allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
		IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
	audiences=[ANDROID_AUDIENCE], 
    scopes=[endpoints.EMAIL_SCOPE])
class HelloWorldApi(remote.Service):
	"""Helloworld API v1."""

	MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
		Greeting,
		times=messages.IntegerField(2, variant=messages.Variant.INT32,
			required=True))

	@endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
		path='hellogreeting/{times}', http_method='POST',
		name='greetings.multiply')
	def greetings_multiply(self, request):
		return Greeting(message=request.message * request.times)

	@endpoints.method(message_types.VoidMessage, GreetingCollection,
						path='hellogreeting', http_method='GET',
						name='greetings.listGreeting')
	def greetings_list(self, unused_request):
		return STORED_GREETINGS

	ID_RESOURCE = endpoints.ResourceContainer(
		message_types.VoidMessage,
		id=messages.IntegerField(1, variant=messages.Variant.INT32))

	@endpoints.method(ID_RESOURCE, Greeting,
						path='hellogreeting/{id}', http_method='GET',
						name='greetings.getGreeting')
	def greeting_get(self, request):
		try:
			return STORED_GREETINGS.items[request.id]
		except (IndexError, TypeError):
			raise endpoints.NotFoundException('Greeting %s not found.' %
				(request.id))

	@endpoints.method(message_types.VoidMessage, Greeting,
		path='hellogreeting/authed', http_method='POST',
		name='greetings.authed')
	def greeting_authed(self, request):
		current_user = endpoints.get_current_user()
		email = (current_user.email() if current_user is not None else 'Anonymous')
		return Greeting(message='hello %s' % (email))

APPLICATION = endpoints.api_server([HelloWorldApi])