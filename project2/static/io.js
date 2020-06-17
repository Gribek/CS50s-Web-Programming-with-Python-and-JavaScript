document.addEventListener('DOMContentLoaded', () => {

    let channel_name = document.querySelector('h4').dataset.channel;
    localStorage.setItem('channel', channel_name);

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
                    'user': localStorage.getItem('name'),
                    'channel': channel_name
                });
            }
            return false;
        };
    });

    // Add message to channel when announce message event
    socket.on('announce message', data => {
        if (data.channel === channel_name) {
            const li = document.createElement('li');
        li.innerHTML = `${data.user}: ${data.message}`;
        document.querySelector('#messages').append(li);
        }
    })
});