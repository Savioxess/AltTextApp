let passwordInput = document.getElementById("password")
let buttonImage = document.getElementById("passwordShowHideIcon")
let confirmPasswordInput = document.getElementById("password-confirm")
let confirmButtonImage = document.getElementById("passwordShowHideIcon-confirm")
let isHidden = true
let isHiddenConfirm = true

function showHidePassword() {
    if(isHidden) {
        passwordInput.type = "text"
        isHidden = false
        buttonImage.src = "/static/images/hide.png"
    } else {
        passwordInput.type = "password"
        isHidden = true
        buttonImage.src = "/static/images/view.png"
    }
}

function showHideConfirmPassword() {
    if(isHiddenConfirm) {
        confirmPasswordInput.type = "text"
        isHiddenConfirm = false
        confirmButtonImage.src = "/static/images/hide.png"
    } else {
        confirmPasswordInput.type = "password"
        isHiddenConfirm = true
        confirmButtonImage.src = "/static/images/view.png"
    }
}
