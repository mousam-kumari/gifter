function generateGiftIdea() {
    const form = document.getElementById('giftForm');
    const formData = new FormData(form);

    const data = {
        age: formData.get('age'),
        gender: formData.get('gender'),
        occasion: formData.get('occasion'),
        recipient_type: formData.get('recipient_type'),
        price_range: formData.get('price_range'),
        categories: []
    };

    // Get all selected categories
    form.querySelectorAll('input[name="categories"]:checked').forEach(checkbox => {
        data.categories.push(checkbox.value);
    });

    fetch('/generate_gift_idea', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';
        if (data.error) {
            resultsDiv.textContent = `Error: ${data.error}`;
        } else {
            data.gift_ideas.forEach(idea => {
                const p = document.createElement('p');
                p.textContent = idea;
                resultsDiv.appendChild(p);
            });
        }
    })
    .catch(error => console.error('Error:', error));
}

function searchGiftIdea() {
    const searchInput = document.getElementById('searchInput').value;

    fetch('/search_gift_idea', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt: searchInput })
    })
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';
        if (data.error) {
            resultsDiv.textContent = `Error: ${data.error}`;
        } else {
            data.gift_ideas.forEach(idea => {
                const p = document.createElement('p');
                p.textContent = idea;
                resultsDiv.appendChild(p);
            });
        }
    })
    .catch(error => console.error('Error:', error));
}
