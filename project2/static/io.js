document.addEventListener('DOMContentLoaded', () => {

    // Get user and channel name
    const channel_name = document.querySelector('h4').dataset.channel;
    const user_name = localStorage.getItem('name')

    // Save name of the channel in local storage
    localStorage.setItem('channel', channel_name);

    function add_message(data) {
        const li = document.createElement('li');
        li.innerHTML = `${data.timestamp}; ${data.user}: ${data.message} `;
        if (data.user === user_name) {
            const button = document.createElement('button');
            button.innerHTML = 'Delete';
            button.dataset.messageId = data.id;
            li.appendChild(button);
        }
        document.querySelector('#messages').append(li);
    }

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Configure submit button
    socket.on('connect', () => {

        // Emit send message event
        document.querySelector('#form_message').onsubmit = () => {
            const input = document.querySelector('#text_message')
            const message = input.value;
            input.value = '';
            if (message.length > 0) {
                socket.emit('send message', {
                    'message': message,
                    'user': user_name,
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