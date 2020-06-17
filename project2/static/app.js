document.addEventListener('DOMContentLoaded', () => {
    // Get two html sections
    let intro_section = document.querySelector('#introduction')
    let channels_section = document.querySelector('#channels')

    // Check if user name is in local storage, hide channels section if not
    if (!localStorage.getItem('name')) {
        intro_section.hidden = false;
        channels_section.hidden = true;

        // When user submit name save it to the local storage and display channels section
        document.querySelector('#form').onsubmit = () => {
            let name = intro_section.querySelector('input').value
            localStorage.setItem('name', name);
            intro_section.hidden = true;
            channels_section.hidden = false;
            return false;
        }
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