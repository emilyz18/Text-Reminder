function addButton() {
    let submitButton = document.getElementById("Submit Button")
    submitButton.addEventListener("click", function() {
        var phoneNumber = document.getElementById("Phone Number").value
        var time = document.getElementById("Time").value
        var notificationTime = document.getElementById("Notification Time").value
        const rtArray = [phoneNumber, time, notificationTime]
        return rtArray
    })

}