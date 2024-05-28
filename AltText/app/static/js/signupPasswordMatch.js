let password = document.getElementById("password")
let confirmPassword = document.getElementById("password-confirm")
let signupButton = document.getElementById("signupButton")

password.addEventListener("input", matchPasswords)
confirmPassword.addEventListener("input", matchPasswords)

function matchPasswords() {
    if(password.value == "") {
        signupButton.disabled = true
        signupButton.style.opacity = "50%"
        signupButton.style.cursor = "default"
        return
    }

    if(password.value == confirmPassword.value) {
        signupButton.disabled = false
        signupButton.style.opacity = "100%"
        signupButton.style.cursor = "pointer"
    } else {
        signupButton.disabled = true
        signupButton.style.opacity = "50%"
        signupButton.style.cursor = "default"
    }
}

matchPasswords()