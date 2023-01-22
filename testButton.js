function addButton() {
  document.getElementById("error").innerText = ""
  var phoneNumber = document.getElementById("Phone Number").value;
  var time = document.getElementById("Time").value;
  var content = document.getElementById("Content").value;
  if (document.getElementById("daysblock") != null) {
    var recurDays = [document.getElementById("Monday").value,
    document.getElementById("Tuesday").value,
    document.getElementById("Wednesday").value,
    document.getElementById("Thursday").value,
    document.getElementById("Friday").value,
    document.getElementById("Saturday").value,
    document.getElementById("Sunday").value]
    const allEqual = recurDays.every(v => v == "false")
    if (allEqual && text == 'weekly') {
      document.getElementById("error").innerText = "must select at least one"

    } else {
      document.getElementById("error").innerText = ""
    }
  }
  var id = document.getElementById("Recurence Dropdown")

  var text = id.options[id.selectedIndex].text;

  var recurFreq = document.getElementById("recurence frequency").value;


  let hr = "";
  let min = "";
  let month = "";
  let day = "";
  let year = "";

  if (time) {
    let timeSplit = time.split("T");
    let date = timeSplit[0].split("-");
    year = date[0];
    month = date[1];
    day = date[2];

    let hrmin = timeSplit[1].split(":");
    hr = hrmin[0];
    min = hrmin[1];

  }

  let randString = makeid(20).toString();
  let newjsonObj = {
    [randString]: {
      'content': content,
      'phoneNumber': phoneNumber,
      'hour': hr,
      'minute': min,
      'month': month,
      'day': day,
      'year': year,
      "recurrence": text,
      "recurFreq": recurFreq,
      'recurDays': recurDays
    }
  }


  console.log(randString);
  console.log(JSON.stringify(newjsonObj));

  // Send the data to the server
  let xhr = new XMLHttpRequest;
  xhr.onerror = event => {
    document.getElementById("error").innerText = 'Failed to send data to server'
  }
  xhr.onload = event => {
    if (xhr.status == 204) document.getElementById("error").innerText = ''
    else if (xhr.status == 400) document.getElementById("error").innerText = 'Invalid settings rejected by server'
    else if (xhr.status >= 500) document.getElementById("error").innerText = `Server error ${xhr.status}`
    else document.getElementById("error").innerText = `Unknown status code ${xhr.status}`
  }

  xhr.open('POST', 'http://localhost:8080', true);
  xhr.send(JSON.stringify(newjsonObj));
}



function checkbox(p) {
  if (document.getElementById(p).value == "false") {
    document.getElementById(p).value = true;
  } else {
    document.getElementById(p).value = false;
  }
}

function changeFunc(i) {
  let code = '<div id = "daysblock">' +
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
    '<label for="Sunday">Sunday</label><br><br>' +
    '</div>';


  if (i == 'weekly') {
    document.getElementById("main").innerHTML += code;
    document.getElementById("Recurence Dropdown").value = "weekly";
  } else {
    if ((document.getElementById("daysblock")) != null) {
      document.getElementById("daysblock").remove();
    }
  }

}

function makeid(length) {
  var result = '';
  var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}