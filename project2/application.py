import os
from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for, \
    abort
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Maximum number of messages stored per channel
CHANNEL_MAX_MESSAGES = 100

# List of all available channels
channels = {}


class Channel:
    """Represents a single channel"""

    def __init__(self, name):
        self.__name = name
        self.__storage_full = False
        self.messages = []

    def __str__(self):
        return self.__name

    # @property
    # def name(self):
    #     return self.__name

    def add_message(self, author, text, timestamp):
        """Save new message"""

        # Create and save new message
        m = Message(author, text, timestamp)
        self.messages.append(m)

        # Check if the messages limit has been reached
        if self.__storage_full:
            del self.messages[0]
        else:
            if len(self.messages) == CHANNEL_MAX_MESSAGES:
                self.__storage_full = True


class Message:
    """Represents a single message"""

    def __init__(self, author, text, timestamp):
        self.author = author
        self.text = text
        self.timestamp = timestamp


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html', channels=channels.values())


@app.route('/channel', methods=('get', 'post'))
def new_channel():
    """Create a new channel"""

    if request.method == 'POST':
        error = None

        # Get user input
        channel_name = request.form.get('channel_name')

        # Form validation
        if not channel_name:
            error = 'Enter channel name'
        elif channel_name in channels.keys():
            error = 'Channel already exists'

        # Create channel if no error
        if error is None:
            ch = Channel(channel_name)
            channels[f'{channel_name}'] = ch

            return redirect(url_for('index'))

        # Display error in form
        flash(error)

    return render_template('new_channel.html')


@app.route('/channel/<string:channel_name>')
def channel_view(channel_name):
    """Display channel with all saved messages"""

    try:
        channel = channels[channel_name]
    except KeyError:
        abort(404)
    else:
        return render_template('view_channel.html', channel=channel)


@socketio.on('send message')
def message(data):
    """Receive new message and broadcast it with timestamp"""

    # Add date and time to message data
    date = datetime.now().strftime("%d %B %Y, %H:%M")
    data['timestamp'] = date

    # Save message
    save_message(data)

    # Broadcast message to users
    emit('announce message', data, broadcast=True)


def save_message(data):
    """Store message for channel"""

    # Get the selected channel
    channel = channels[data['channel']]

    # Save new message
    channel.add_message(author=data['user'], text=data['message'],
                        timestamp=data['timestamp'])
