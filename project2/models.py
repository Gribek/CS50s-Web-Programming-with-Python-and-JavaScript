# Maximum number of messages stored per channel
CHANNEL_MAX_MESSAGES = 100


class Channel:
    """Represents a single channel"""

    def __init__(self, name):
        self.__name = name
        self.messages = []
        self.__message_count = 0

    def __str__(self):
        return self.__name

    def add_message(self, author, text, timestamp):
        """Save new message"""

        # Create and save new message
        m = Message(self.__message_count, author, text, timestamp)
        self.messages.append(m)
        self.__message_count += 1

        # If the message limit has been reached, delete the oldest one
        if self.__message_count > CHANNEL_MAX_MESSAGES:
            del self.messages[0]

        return self.__message_count - 1

    def delete_message(self, message_id):
        """Delete selected message"""

        for m in self.messages:
            if m.id == int(message_id):
                self.messages.remove(m)
                break


class Message:
    """Represents a single message"""

    def __init__(self, message_id, author, text, timestamp):
        self.__id = message_id
        self.author = author
        self.text = text
        self.timestamp = timestamp

    @property
    def id(self):
        return self.__id
