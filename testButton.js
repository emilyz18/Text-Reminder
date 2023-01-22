function addButton() {
        var phoneNumber = document.getElementById("Phone Number").value;
        var time = document.getElementById("Time").value;
        var notificationTime = document.getElementById("Notification Time").value;
        var content = document.getElementById("Content").value;
        var phoneNumber = document.getElementById("Phone Number").value
        var time = document.getElementById("Time").value
        var notificationTime = document.getElementById("Notification Time").value
        var content = document.getElementById("Content").value
        var recurDays = [document.getElementById("Monday").value,
                         document.getElementById("Tuesday").value,
                         document.getElementById("Wednesday").value,
                         document.getElementById("Thursday").value,
                         document.getElementById("Friday").value,
                         document.getElementById("Saturday").value,
                         document.getElementById("Sunday").value]

        const rtArray = [phoneNumber, time, notificationTime, content, recurDays]

        // Convert array to JSON format
        const keys = ["phoneNumber", "time", "notificationTime", "content", "recurDays"]
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


function checkbox(p){
    document.getElementById(p).value = true
}
