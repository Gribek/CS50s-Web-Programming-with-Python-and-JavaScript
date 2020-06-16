import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Maximum number of messages stored per channel
CHANNEL_MAX_MESSAGES = 100


class Channel:
    """Represents a single channel"""

    def __init__(self, name):
        self.__name = name
        self.__storage_full = False
        self.messages = []

    def __str__(self):
        return self.__name

    def add_message(self, author, text):
        """Save new message"""

        # Create and save new message
        m = Message(author, text)
        self.messages.append(m)

        # Check if the messages limit has been reached
        if self.__storage_full:
            del self.messages[0]
        else:
            if len(self.messages) == CHANNEL_MAX_MESSAGES:
                self.__storage_full = True


class Message:
    """Represents a single message"""

    def __init__(self, author, text):
        self.author = author
        self.text = text


@app.route("/")
def index():
    return render_template('index.html')
