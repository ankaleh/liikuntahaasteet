var getMessage = () => {
    var node = document.createTextNode("{{message}}")
    var element = document.getElementById("notification")
    "{% if message.tags %}"
        element.classList.add("{{ message.tags }}")
    "{% endif %}"
    element.appendChild(node)

    setTimeout(() => {
        element.removeAttribute("class")
        element.removeChild(node)
    }, 3000)

}

var myFunction = () => {
    alert('huhuu')
}

