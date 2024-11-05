window.addEventListener('load', () => {
    // grab the devices
    console.log("loading");
    httpReq(`/api/device/list`, "GET", true)
        .then((response) => {
            if (response) {
                let devices = response.devices;
                // devices is an array of objects, convert to array of arrays
                const table = new DataTable('#device-log-table', {
                    // default entries per page
                    data: devices,
                    columns: [
                        { data: 'id' },
                        { data: 'device_name' },
                        { data: 'model' },
                        { data: 'serial_number' },
                        { data: 'device_owner' },
                        { data: 'device_location' },
                        { data: 'manufacturer' },

                        { data: 'last_action' },
                        { data: 'last_action_description' },
                        { data: 'last_action_timestamp' },

                        // TODO: Update past here
                        // { data: 'firmware_version' },
                        // { data: 'last_log_id' },
                        // { data: 'last_log_id' },

                        // <th>Last Action</th>
                        // <th>Action Description</th>
                        // <th>Action Timestamp</th>

                        // <th>Device ID</th>
                        // <th>Device Name</th>
                        // <th>Device Model</th>
                        // <th>Device Serial</th>
                        // <th>Device Owner</th>
                        // <th>Device Location</th>
                        // <th>Device Manufacturer</th>
                        // <th>Last Action</th>
                        // <th>Action Description</th>
                        // <th>Action Timestamp</th>
                    ],
                });
            }
        }).catch((error) => {
            console.error(error);
        }).finally(() => {
            // device-log-table-loader hide this id
            const loader = document.getElementById('device-log-table-loader');
            // get the parent of the loader
            const parent = loader.parentElement;
            parent.style.display = 'none';
        });
});
