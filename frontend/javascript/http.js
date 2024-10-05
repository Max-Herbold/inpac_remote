ENDPOINT = ".";

function _generateErrorResponse(xmlHttp) {
    if (xmlHttp.responseText) {
        try {
            return JSON.parse(xmlHttp.responseText);
        } catch (error) {
            return { "response": xmlHttp.responseText, "error": "JSON parsing error" }
        }
    } else {
        return xmlHttp.statusText;
    }
}

function httpReq(url, method = "GET", async = false, headers = null, body = null) {
    // add the prefix to the url
    url = ENDPOINT + url;

    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open(method, url, async);

    // if headers then set them
    if (headers) {
        for (var key in headers) {
            xmlHttp.setRequestHeader(key, headers[key]);
        }
    }

    // if body is defined as a json object
    if (body) {
        xmlHttp.send(JSON.stringify(body));
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
                        logError(`Status: ${xmlHttp.status}, StatusText: ${xmlHttp.statusText}, Response: ${xmlHttp.responseText}`);
                        reject(_generateErrorResponse(xmlHttp));
                    }
                }
            };
            try {
                xmlHttp.send(null);
            } catch (error) {
                logError(error);
                reject(_generateErrorResponse(xmlHttp));
            }
        });
    } else {
        try {
            xmlHttp.send(null);
            if (xmlHttp.status == 200) {
                return JSON.parse(xmlHttp.responseText);
            } else {
                logError(`Status: ${xmlHttp.status}, StatusText: ${xmlHttp.statusText}`);
                return _generateErrorResponse(xmlHttp);
            }
        } catch (error) {
            logError(error);
            return _generateErrorResponse(xmlHttp);
        }
    }
}
