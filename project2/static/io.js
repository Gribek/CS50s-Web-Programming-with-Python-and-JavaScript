document.addEventListener('DOMContentLoaded', () => {

    // Get user and channel name
    const channel_name = document.querySelector('h4').dataset.channel;
    const user_name = localStorage.getItem('name')

    // Save name of the channel in local storage
    localStorage.setItem('channel', channel_name);

    function add_message(data) {
        const li = document.createElement('li');
        li.innerHTML = `${data.timestamp}; ${data.author}: ${data.text} `;
        if (data.author === user_name) {
            const button = document.createElement('button');
            button.innerHTML = 'Delete';
            button.dataset.messageId = data._Message__id;
            li.appendChild(button);
        }
        document.querySelector('#messages').append(li);
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
        else {

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
    })
});