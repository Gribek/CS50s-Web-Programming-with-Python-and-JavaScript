document.addEventListener('DOMContentLoaded', () => {

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
                socket.emit('send message', {'message': message});
            }
            return false;
        };
    });

    // Add message to channel when announce vote event
    socket.on('announce message', data => {
        const li = document.createElement('li');
        li.innerHTML = data.message;
        document.querySelector('#messages').append(li);
    })
});