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
            if (name.length > 0) {
                localStorage.setItem('name', name);
                intro_section.hidden = true;
                channels_section.hidden = false;
            }
            return false;
        }
    }

    // Add link to the last visited channel, if any
    let channel = localStorage.getItem('channel')
    if (channel) {
        const link =  document.createElement('a');
        link.setAttribute('href', `/channel/${channel}`);
        link.className += 'btn btn-success btn-sm';
        link.innerHTML = 'Last visited channel';
        document.querySelector('#nav').append(link);
    }
});