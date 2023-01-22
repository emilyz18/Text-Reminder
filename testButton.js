function addButton() {
    document.getElementById("error").innerText = ""
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
    const allEqual = recurDays.every( v => v == "false")
                     console.log(allEqual)
    var id = document.getElementById("Recurence Dropdown")

    var text = id.options[id.selectedIndex].text;
    console.log(text)

    if (allEqual && text == 'weekly') {
        console.log("success")
        document.getElementById("error").innerText = "must select at least one"
        
    } else {
        document.getElementById("error").innerText = ""

}

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
  if (document.getElementById(p).value == "false") {
    document.getElementById(p).value = true;
  } else {
    document.getElementById(p).value = false;
  }
}

function changeFunc(i) {
    let code = '<div id = "daysblock">'+
    '<p>Select the Days you want the reminder to recur on: </p>' +
  '<input type="checkbox" id="Monday" name="Monday" value=false onClick="checkbox(id)">' +
  '<label for="Monday"> Monday</label><br><br>' +
  '<input type="checkbox" id="Tuesday" name="Tuesday" value=false onClick="checkbox(id)">' +
  '<label for="Tuesday"> Tuesday</label><br><br>' +
  '<input type="checkbox" id="Wednesday" name="Wednesday" value=false onClick="checkbox(id)">' +
  '<label for="Wednesday">Wednesday</label><br><br>' +
  '<input type="checkbox" id="Thursday" name="Thursday" value=false onClick="checkbox(id)">' +
  '<label for="Thursday">Thursday</label><br><br>' +
  '<input type="checkbox" id="Friday" name="Friday" value=false onClick="checkbox(id)">' +
  '<label for="Friday">Friday</label><br><br>' +
  '<input type="checkbox" id="Saturday" name="Saturday" value=false onClick="checkbox(id)">' +
  '<label for="Saturday">Saturday</label><br><br>' +
  '<input type="checkbox" id="Sunday" name="Sunday" value=false onClick="checkbox(id)">' +
  '<label for="Sunday">Sunday</label><br><br>'+
  '</div>';


    if (i == 'weekly') {
      document.getElementById("main").innerHTML += code;
      document.getElementById("Recurence Dropdown").value = "weekly";
    } else {
        if ((document.getElementById("daysblock")) != null){
        document.getElementById("daysblock").remove();
        }
    }
    
  }
