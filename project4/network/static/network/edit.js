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

        let csrf_token = getCookie('csrftoken')
        fetch(`/edit_post/${this.dataset.postId}`, {
            method: 'POST',
            body: JSON.stringify(textarea.value),
            headers: {'X-CSRFToken': csrf_token}
        })
            .then(response => {
                if (response.status === 200) {
                    post_text.textContent = textarea.value
                }
                textarea.replaceWith(post_text)
            })

        this.innerHTML = 'Edit'
        this.onclick = post_edit
    }
}


// The following function has been copied from
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}