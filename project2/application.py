import os
from datetime import datetime

from flask import Flask, render_template, request, flash, redirect, url_for, \
    abort, jsonify
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

    channel = get_channel(channel_name)
    if channel is None:
        abort(404)
    else:
        return render_template('view_channel.html', channel=channel)


@app.route('/messages', methods=['post'])
def get_messages():
    """Return all messages for the channel"""

    # Get requested channel
    channel_name = request.form.get('channel')
    channel = get_channel(channel_name)
    if channel is None:
        return jsonify({'success': False})

    # Get all messages
    data = [m.__dict__ for m in channel.messages]

    return jsonify({'success': True, 'messages': data})


@socketio.on('send message')
def message(data):
    """Receive new message and broadcast it with timestamp"""

    # Add date and time to message data
    date = datetime.now().strftime("%d %B %Y, %H:%M")
    data['timestamp'] = date

    # Save message and add id to data
    data['_Message__id'] = save_message(data)

    # Broadcast message to users
    emit('announce message', data, broadcast=True)


@socketio.on('delete message')
def delete_message(data):
    """Receive request to delete message and broadcast it"""

    # Get requested channel
    channel_name = data['channel']
    channel = get_channel(channel_name)

    # Delete selected message
    message_id = data['message_id']
    channel.delete_message(message_id)

    # Broadcast delete message to users
    emit('announce delete', data, broadcast=True)


def save_message(data):
    """Store message for channel"""

    # Get the selected channel
    channel = channels[data['channel']]

    # Save new message
    message_id = channel.add_message(
        author=data['author'], text=data['text'], timestamp=data['timestamp'])

    return message_id


def get_channel(channel_name):
    """Return the selected channel"""

    try:
        channel = channels[channel_name]
    except KeyError:
        channel = None

    return channel
