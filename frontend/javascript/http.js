ENDPOINT = ".";

function httpReq(url, method = "GET", async = false, headers = null) {
    // add the prefix to the url
    url = ENDPOINT + url;

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open(method, url, async);

    // if headers then set them
    if (headers) {
        for (var key in headers) {
            console.log(key, headers[key]);
            xmlHttp.setRequestHeader(key, headers[key]);
        }
    }

    // Error logging function   
    function logError(error) {
        // console.error(`HTTP Error: ${error}`);
    }

    // if async, wait for the response
    if (async) {
        return new Promise((resolve, reject) => {
            xmlHttp.onreadystatechange = function () {
                if (xmlHttp.readyState == 4) {
                    if (xmlHttp.status == 200) {
                        resolve(JSON.parse(xmlHttp.responseText));
                    } else {
                        logError(`Status: ${xmlHttp.status}, StatusText: ${xmlHttp.statusText}`);
                        reject(""); // resolve with null in case of error
                    }
                }
            };
            try {
                xmlHttp.send(null);
            } catch (error) {
                logError(error);
                reject(""); // resolve with null in case of error
            }
        });
    } else {
        try {
            xmlHttp.send(null);
            if (xmlHttp.status == 200) {
                return JSON.parse(xmlHttp.responseText);
            } else {
                logError(`Status: ${xmlHttp.status}, StatusText: ${xmlHttp.statusText}`);
                return null; // return null in case of error
            }
        } catch (error) {
            logError(error);
            return null; // return null in case of error
        }
    }
}
