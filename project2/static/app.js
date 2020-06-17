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
});