function submit() {
  const errorField = document.getElementById('error');
  var time = document.getElementById("Time").value;

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

  function strToBool(str) {
    return str == "true";
  }

  recurrence = document.getElementById("Recurence Dropdown").value;
  recurDays = [
    strToBool(document.getElementById("Sunday").value),
    strToBool(document.getElementById("Monday").value),
    strToBool(document.getElementById("Tuesday").value),
    strToBool(document.getElementById("Wednesday").value),
    strToBool(document.getElementById("Thursday").value),
    strToBool(document.getElementById("Friday").value),
    strToBool(document.getElementById("Saturday").value)
  ];

  let newjsonObj = {
    [makeid(20).toString()]: {
      'message': document.getElementById("Content").value,
      'phone': document.getElementById("Phone Number").value,
      'hour': hr,
      'minute': min,
      'month': month,
      'date': day,
      'year': year,
      "recurrence": recurrence,
      "recurFreq": document.getElementById("recurence frequency").value,
      'recurDays': recurDays
    }
  }

  if (recurrence == 'weekly' && recurDays.indexOf(true) == -1) {
    errorField.innerText = "please select at least one day"
  } else {
    // Send the data to the server
    console.log(JSON.stringify(newjsonObj))
    let xhr = new XMLHttpRequest;
    xhr.onerror = event => {
      errorField.innerText = 'Failed to send data to server'
    }
    xhr.onload = event => {
      if (xhr.status == 204) errorField.innerText = ''
      else if (xhr.status == 400) errorField.innerText = 'Invalid settings rejected by server'
      else if (xhr.status >= 500) errorField.innerText = `Server error ${xhr.status}`
      else errorField.innerText = `Unknown status code ${xhr.status}`
    }

    xhr.open('POST', 'http://localhost:8080', true);
    xhr.send(JSON.stringify(newjsonObj));
  }
}

function recurrenceChange(value) {
  daysblock = document.getElementById('daysblock');
  freqblock = document.getElementById('freqblock');
  if (value == 'once') {
    daysblock.classList.add('hidden');
    freqblock.classList.add('hidden');
  } else if (value == 'daily') {
    daysblock.classList.add('hidden');
    freqblock.classList.remove('hidden');
  } else if (value == 'weekly') {
    daysblock.classList.remove('hidden');
    freqblock.classList.remove('hidden');
  }
}
recurrenceChange(document.getElementById("Recurence Dropdown").value);

function makeid(length) {
  var result = '';
  var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}