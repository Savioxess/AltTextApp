const dropdownMenu = document.getElementById("dropdownMenu")
let dropdownIsOpen = false

document.getElementById("dropdownButton").addEventListener("click", function() {
    if(!dropdownIsOpen) {
        dropdownMenu.classList.remove("hidden")
        dropdownMenu.classList.add("flex")
        dropdownIsOpen = !dropdownIsOpen
    } else {
        dropdownMenu.classList.add("hidden")
        dropdownMenu.classList.remove("flex")
        dropdownIsOpen = !dropdownIsOpen
    }
}) 