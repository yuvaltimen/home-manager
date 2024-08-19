

function compareFn(a, b) {

    const a_check_state = a.getElementsByTagName('input')[0].checked;
    const b_check_state = b.getElementsByTagName('input')[0].checked;

    const a_inner_text = a.children[0].children[0].innerText;
    const b_inner_text = b.children[0].children[0].innerText;

    if (a_check_state === b_check_state) {
        // Both are checked or both are unchecked, compare using innerText
        return a_inner_text.toUpperCase().localeCompare(b_inner_text.toUpperCase());
    } else {
        // Exactly one is checked and should come 2nd
        return a_check_state ? 1 : -1;
    }
}

function sort_checked() {
    if (document.getElementById('the_specific_checkbox_ul') !== null) {
        const ul = document.getElementById('the_specific_checkbox_ul');
        const items = Array.from(ul.getElementsByTagName('LI'));

        items.sort((a, b) => compareFn(a, b));
        // Clear existing list
        ul.innerHTML = '';
        items.forEach(li => ul.appendChild(li));
      }
}

function populate_checkboxes_from_state() {
    if (document.getElementById('the_specific_checkbox_ul') !== null) {
        document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
            const storedState = localStorage.getItem(checkbox.id);
            checkbox.checked = storedState === 'true'; // Convert string to boolean
        });
    }
}

function clear_all() {
    document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
        localStorage.setItem(checkbox.id, false);
    });
    populate_checkboxes_from_state();
    sort_checked();
}

function select_all() {
    document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
        localStorage.setItem(checkbox.id, true);
    });
    populate_checkboxes_from_state();
    sort_checked();
}

function gatherSelectedItems() {
    let selectedIds = [];
    for (var i = 0; i < localStorage.length; i++) {
        if (localStorage.key(i).startsWith("checkbox_")
        && (localStorage.getItem(localStorage.key(i)) == 'true')) {
            selectedIds.push(localStorage.key(i));
        }
    }
    document.getElementById('item_ids').value = selectedIds.join(',');
    console.log(selectedIds.join(','));
}


// Wait for window.onload for all DOM elements to be created
window.addEventListener('load', function() {
    if (document.getElementById('the_specific_checkbox_ul') !== null) {
        document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
                checkbox.addEventListener('change', function(checkbox) {
                    console.log("Writing to localStorage");
                    localStorage.setItem(checkbox.id, checkbox.checked);
                    sort_checked();
                });
            }
        );
    }
    if (document.querySelector('#groceryitem_delete_multi_form') !== null) {
        document.querySelector('#groceryitem_delete_multi_form').addEventListener('submit', gatherSelectedItems);
    }
    populate_checkboxes_from_state();
    sort_checked();
});







