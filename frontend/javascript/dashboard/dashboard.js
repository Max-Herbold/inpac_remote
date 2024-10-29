function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}


// on load
// window.addEventListener('load', () => {
//     // grab the devices
//     httpReq(`/api/device/list`, "GET", true)
//         .then((response) => {
//             if (response) {
//                 let devices = response.devices;
//                 let deviceTable = document.getElementById("device-table");
//                 let tableHtml = `<tr>
//                     <th>Device Name</th>
//                     <th>Device Model</th>
//                     <th>Device Manufacturer</th>
//                     <th>Device Serial Number</th>
//                     <th>Device Owner</th>
//                     <th>Device Location</th>
//                     <th>Additional Notes</th>
//                 </tr>`;

//                 devices.forEach((device) => {
//                     tableHtml += `<tr>
//                         <td>${device.device_name}</td>
//                         <td>${device.model}</td>
//                         <td>${device.device_manufacturer}</td>
//                         <td>${device.serial_number}</td>
//                         <td>${device.device_owner}</td>
//                         <td>${device.device_location}</td>
//                         <td>${device.additional_notes}</td>
//                     </tr>`;
//                 });

//                 deviceTable.innerHTML = tableHtml;
//             }
//         }).catch((error) => {
//             console.error(error);
//         });
// });