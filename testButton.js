function addButton() {
        var phoneNumber = document.getElementById("Phone Number").value;
        var time = document.getElementById("Time").value;
        var notificationTime = document.getElementById("Notification Time").value;
        var content = document.getElementById("Content").value;
        const rtArray = [phoneNumber, time, notificationTime, content]

        // Convert array to JSON format
        const keys = ["phoneNumber", "time", "notificationTime", "content"]
        let jsonObj = convertToJSON(keys, rtArray);
        
        console.log(jsonObj);
}

function convertToJSON(keys, values) {
    let jsonObj = {};

    values.map((elem, index) => {
        let key = keys[index];
        return jsonObj[key] = elem;
    })

    jsonObj = JSON.stringify(jsonObj);

    return jsonObj;
}
