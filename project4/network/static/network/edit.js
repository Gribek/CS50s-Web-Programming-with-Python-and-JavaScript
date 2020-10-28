document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit').forEach(button => {
        button.onclick = post_edit
    })
});

function post_edit() {
    let post_text = this.parentElement.querySelector('.text')
    let textarea = document.createElement('textarea')
    textarea.textContent = post_text.textContent
    post_text.replaceWith(textarea)

    this.innerHTML = 'Save'
    this.onclick = function () {
        // TODO:save changes
        post_text.textContent = textarea.textContent
        textarea.replaceWith(post_text)
        this.innerHTML = 'Edit'
        this.onclick = post_edit
    }
}