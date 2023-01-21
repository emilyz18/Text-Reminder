windows.onload = function() {
    addButton()
}

function addButton() {
    let submitButton = document.getElementById("Submit Button")
    submitButton.addEventListener("click", function() {
        var phoneNumber = document.getElementById("Phone Number").value
        var time = document.getElementById("Time").value
        var notificationTime = document.getElementById("Notification Time").value
        var content = document.getElementById("Content").value
        const rtArray = [phoneNumber, time, notificationTime, content]
        return rtArray
    })

}
