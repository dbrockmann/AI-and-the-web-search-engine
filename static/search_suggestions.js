
document.addEventListener('DOMContentLoaded', () => {
    const search_input = document.getElementById('search-input');
    const list = document.getElementById('search-suggestions-list');
  
    const update_list = () => {
        const value = search_input.value;
    
        // fetch suggestion data and update list
        fetch(`${window.location.origin}/search-suggestions?q=${encodeURIComponent(value)}`).then(response => {
            if (!response.ok) throw new Error('Incorrect response');
            return response.json();
        }).then(data => {

            // clear list
            list.innerHTML = '';

            // add new list items
            data.forEach(item => {
                const listItem = document.createElement('li');
                listItem.innerText = item;
                listItem.addEventListener('click', () => {
                    window.open(`/search-results?q=${encodeURIComponent(item)}`, '_self')
                })

                list.appendChild(listItem);
            });

        }).catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    };

    // attach event listener to search field
    search_input.addEventListener('input', update_list)
    search_input.addEventListener('focus', update_list)
});
  
