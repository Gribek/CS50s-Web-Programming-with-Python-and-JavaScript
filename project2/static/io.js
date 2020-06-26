document.addEventListener('DOMContentLoaded', () => {

    // Get user and channel name
    const channel_name = document.querySelector('h4').dataset.channel;
    const user_name = localStorage.getItem('name')

    // Save name of the channel in local storage
    localStorage.setItem('channel', channel_name);

    // Adding messages
    function add_message(data) {
        const div = document.createElement('div');
        div.innerHTML = `<span class="date">${data.timestamp}</span><br><span class="author">${data.author}</span>: ${data.text}`;
        div.dataset.messageId = data._Message__id;
        if (data.author === user_name) {
            const button = document.createElement('button');
            button.innerHTML = 'X';
            button.className += 'delete';
            // button.dataset.messageId = data._Message__id;
            button.addEventListener('click', emit_delete)
            div.appendChild(button);
        }
        document.querySelector('#messages').append(div);
        window.scrollTo(0,document.body.scrollHeight);
    }


    // Deleting messages
    function delete_message(message_id) {
        const element = document.querySelector(`[data-message-id="${message_id}"]`)
        element.remove();
    }


    // Loading messages
    // Create new request
    const request = new XMLHttpRequest();
    request.open('POST', '/messages');

    // Callback function when request completes
    request.onload = () => {
        const data = JSON.parse(request.responseText);

        if (data.success) {
            data.messages.forEach(add_message)
        }
    }

    // Add data to send with request form
    const form = new FormData();
    form.append('channel', channel_name);

    // Send request
    request.send(form);


    // SocketIO - messages sending/receiving
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Configure submit button
    socket.on('connect', () => {

        // Emit send message event
        document.querySelector('#form_message').onsubmit = () => {
            const input = document.querySelector('#text_message')
            const text = input.value;
            input.value = '';
            if (text.length > 0) {
                socket.emit('send message', {
                    'text': text,
                    'author': user_name,
                    'channel': channel_name
                });
            }
            return false;
        };
    });

    // Add message to channel when announce message event
    socket.on('announce message', data => {
        if (data.channel === channel_name) {
            add_message(data);
        }
    });

    // Emit delete message event
    function emit_delete(event) {

        // Selected button
        const element = event.target;

        // Emit delete message event
        socket.emit('delete message', {
            'channel': channel_name,
            'message_id': element.parentElement.dataset.messageId
        });
    }

    // Delete message from channel when announce delete event
    socket.on('announce delete', data => {
        if (data.channel === channel_name) {
            delete_message(data.message_id);
        }
    });
});