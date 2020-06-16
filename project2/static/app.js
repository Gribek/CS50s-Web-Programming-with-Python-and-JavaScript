document.addEventListener('DOMContentLoaded', () => {
    let intro_section = document.querySelector('#introduction')
    let channels_section = document.querySelector('#channels')

    if (!localStorage.getItem('name')) {
        intro_section.hidden = false;
        channels_section.hidden = true;

        document.querySelector('#form').onsubmit = () => {
            let name = intro_section.querySelector('input').value
            localStorage.setItem('name', name);
            intro_section.hidden = true;
            channels_section.hidden = false;
            return false;
        }
    }
})