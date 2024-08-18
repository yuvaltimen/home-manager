const ul_to_sort_name = 'the_specific_checkbox_ul';


function compareFn(a, b) {
    if (a.getElementsByTagName('input')[0].checked === b.getElementsByTagName('input')[0].checked) {
        // Both are checked or both are unchecked, compare using innerText
        return a.children[0].children[0].innerText < a.children[0].children[0].innerText;
    } else {
        // Exactly one is checked and should come 2nd
        return a.getElementsByTagName('input')[0].checked ? 1 : -1;
    }
}

function sort_checked() {
    if (document.getElementById(ul_to_sort_name)) {
        const ul = document.getElementById(ul_to_sort_name);

        Array.from(ul.getElementsByTagName('LI'))
          .sort((a, b) => compareFn(a, b))
          .forEach(li => ul.appendChild(li));
      }
}

document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
    checkbox.addEventListener('change', function() {
        localStorage.setItem(checkbox.id, checkbox.checked);
    });

    checkbox.addEventListener('change', function() {
        sort_checked();
    });
    }
);

window.addEventListener('load', function() {
    document.querySelectorAll('input[type="checkbox"]').forEach(function(checkbox) {
        const storedState = localStorage.getItem(checkbox.id);
        checkbox.checked = storedState === 'true'; // Convert string to boolean
    });
    sort_checked();
});



