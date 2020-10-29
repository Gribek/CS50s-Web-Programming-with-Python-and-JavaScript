document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like').forEach(button => {
        button.onclick = function () {
            let counter_el = this.parentElement.querySelector('span')
            let counter = counter_el.innerText
            if (this.innerHTML.trim() === 'Like') {
                 fetch(`/like/${this.dataset.postId}`)
                     .then(() => {
                         this.innerHTML = 'Unlike'
                         counter++
                         counter_el.innerText = counter
                     })
            }
            else
            {
                fetch(`/unlike/${this.dataset.postId}`)
                     .then(() => {
                         this.innerHTML = 'Like'
                         counter--
                         counter_el.innerText = counter
                     })
            }
        }
    })
})
