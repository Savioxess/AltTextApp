document.getElementById("imageInput").addEventListener("change", (event) => {
    const file = event.target.files[0];

    console.log(file)

    if(file) {
        const reader = new FileReader()
        reader.onload = function(e) {
            document.getElementById("inputContainer").style.display = "none"
            const img = document.getElementById("imagePreview")
            img.parentElement.style.display = "block"
            img.src = e.target.result
            img.alt = file.name.replace(/\.[^/.]+$/, "")
        }

        reader.readAsDataURL(file)
    }
})