var form = document.getElementById('searchForm');
console.log("testing")
form.addEventListener('submit', function (event) {
    event.preventDefault()

    var searchValue = document.getElementById('form-search').value

    if ( searchValue.length <  1) {
        alert('please enter some text')
    } else {
        alert(searchValue)
    }
})