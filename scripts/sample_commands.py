import interactions
from resources import env
import random

@interactions.listen("on_message_create")
async def name_this_however_you_want(message_create: interactions.events.MessageCreate):
    # Whenever we specify any other event type that isn't "READY," the function underneath
    # the decorator will most likely have an argument required. This argument is the data
    # that is being supplied back to us developers, which we call a data model.

    # In this example, we're listening to messages being created. This means we can expect
    # a "message_create" argument to be passed to the function, which will contain the
    # data model for the message

    # We can use the data model to access the data we need.
    # Keep in mind that you can only access the message content if your bot has the MESSAGE_CONTENT intent.
    # You can find more information on this in the migration section of the quickstart guide.
    message: interactions.Message = message_create.message
    print(f"We've received a message from {message.author.username}. The message is: {message.content}.")
