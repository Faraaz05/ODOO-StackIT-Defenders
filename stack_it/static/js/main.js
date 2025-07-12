function showAlert() {
    alert('This is a placeholder action!');
}

function vote(type, id, value) {
    fetch('/questions/vote/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({vote_type: type, id: id, value: value})
    })
    .then(response => {
        if (response.status === 403) {
            window.location = '/accounts/login/';
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data.upvotes !== undefined) {
            // Calculate net votes (upvotes - downvotes)
            const netVotes = data.upvotes - Math.abs(data.downvotes);
            
            if (type === 'question') {
                document.getElementById('q-votes-' + id).innerText = netVotes;
            } else if (type === 'answer') {
                document.getElementById('a-votes-' + id).innerText = netVotes;
            }
            
            // Update button highlighting
            const group = document.getElementById(type.charAt(0) + '-vote-group-' + id);
            if (group) {
                const upvoteBtn = group.querySelector('.vote-btn:first-of-type');
                const downvoteBtn = group.querySelector('.vote-btn:last-of-type');
                
                // Remove all vote classes first
                upvoteBtn.classList.remove('voted-up', 'voted-down');
                downvoteBtn.classList.remove('voted-up', 'voted-down');
                
                // Apply the correct highlighting based on user_vote
                if (data.user_vote === 1) {
                    upvoteBtn.classList.add('voted-up');
                } else if (data.user_vote === -1) {
                    downvoteBtn.classList.add('voted-down');
                }
                // If user_vote is 0, no highlighting (both buttons are grey)
            }
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}