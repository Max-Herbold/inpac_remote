function submitLogForm() {
    // grab the fields we care about
    let device_location = document.getElementById("device_location").value;
    let device_action = document.getElementById("device_action").value;
    let device_model = document.getElementById("device_model").value
    let device_manufacturer = document.getElementById("device_manufacturer").value;
    let device_serial_number = document.getElementById("device_serial_number").value;
    let device_name = document.getElementById("device_name").value;

    headers = {
        "device_location": device_location,
        "device_action": device_action,
        "device_model": device_model,
        "device_manufacturer": device_manufacturer,
        "device_serial_number": device_serial_number,
        "device_name": device_name
    }

    httpReq(`/api/device/add`, "POST", true, headers = headers).then((response) => {
        console.log(response);
    }).catch((error) => {
        console.error(error);
    });

    // FIXME: This form still redirects on submission... why?
    return false;
}



{/* <form onsubmit="return false;" class="form-container">
<h1>Create Device Log</h1>
<!-- location -->
<label for="location"><b>Location</b></label>
<input type="text" placeholder="Enter Location" name="device_location" required>

<!-- device log action, move/install/repair/discard -->
<label for="device_action"><b>Device Action</b></label>
<select name="device_action" id="device_action">
  <option value="move">Move</option>
  <option value="create">New Device</option>
  <option value="repair">Repair</option>
  <option value="discard">Discard</option>
</select>

<label for="device_model"><b>Device Model</b></label>
<input type="text" placeholder="Enter Device Model" name="device_model" required>

<!-- manufacturer -->
<label for="device_manufacturer"><b>Manufacturer</b></label>
<input type="text" placeholder="Enter Manufacturer" name="device_manufacturer" required>

<!-- device serial number field -->
<label for="device_serial_number"><b>Device Serial</b></label>
<input type="text" placeholder="Enter Device Serial" name="device_serial_number">

<!-- device name field -->
<label for="device_name"><b>Device Name</b></label>
<input type="text" placeholder="Enter Device Name" name="device_name"> */}
