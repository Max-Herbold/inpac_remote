ENDPOINT = ".";

function httpGet(url, async = false) {
    // add the prefix to the url
    url = ENDPOINT + url;

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, async);

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
