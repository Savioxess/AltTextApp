const saveForm = document.getElementById("saveForm")
const saveButton = document.getElementById("saveButton")
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content')
const infoDisplay = document.getElementById("infoDisplay")

saveForm.addEventListener("submit", async function(e) {
    e.preventDefault();
    saveButton.disabled = true
    saveButton.classList.remove("saveButton")
    saveButton.classList.add("disabledSaveButton")

    const saveData = {
        "file_name": e.target.fileName.value,
        "text": e.target.response.value
    }

    const response = await fetch("http://127.0.0.1:8000/saveText/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(saveData)
    })

    try {
        const parsedResponse = await response.json()

        if(parsedResponse.error) {
            const errorText = `<h1 class="error">${parsedResponse.error}</h1>`
            infoDisplay.innerHTML = errorText
            setTimeout(endCooldown, 2000)
            return
        }       
        
        const successText = `<h1 class="success">${parsedResponse.success}</h1>`
        infoDisplay.innerHTML = successText
        setTimeout(endCooldown, 3000)
    } catch(error) {
        console.log(error)
    }
})

function endCooldown() {
    infoDisplay.innerHTML = ""
    saveButton.disabled = false
    saveButton.classList.add("saveButton")
    saveButton.classList.remove("disabledSaveButton")
}