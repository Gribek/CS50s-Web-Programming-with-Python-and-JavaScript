document.addEventListener('DOMContentLoaded',  () => {
    const button = document.querySelector('#follow');
    button.onclick = () => {
        if (button.innerHTML.trim() === 'Follow') {
             fetch(`/follow/${button.dataset.userId}`)
                 .then(() => {button.innerHTML = 'Unfollow'})
        }
        else
        {
            fetch(`/unfollow/${button.dataset.userId}`)
                .then(() => {button.innerHTML = 'Follow'})
        }
    };
});