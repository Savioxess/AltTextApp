const changeImageButton = document.getElementById("changeImageButton")

document.getElementById("imageInput").addEventListener("change", (event) => {
    const file = event.target.files[0];
    changeImageButton.classList.remove("hidden")

    if(file) {
        const reader = new FileReader()
        reader.onload = function(e) {
            document.getElementById("inputContainer").style.display = "none"
            const img = document.getElementById("imagePreview")
            img.parentElement.style.display = "block"
            base64EncodedImage = e.target.result
            img.src = e.target.result
            img.alt = file.name.replace(/\.[^/.]+$/, "")
        }

        reader.readAsDataURL(file)
    }
})