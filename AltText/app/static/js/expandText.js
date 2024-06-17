function expand(filename) {
    const expandText = document.getElementById(filename).querySelector("#expand")
    const image = document.getElementById(filename).querySelector("button").querySelector("img")
    console.log(image)

    if(expandText.classList.contains("hidden")) {
        expandText.classList.remove("hidden")
        image.alt = "hide-text"
        image.src = "/static/images/reduce.png"
    } else {
        expandText.classList.add("hidden")
        image.alt = "show-text"
        image.src = "/static/images/expand.png"
    }
}