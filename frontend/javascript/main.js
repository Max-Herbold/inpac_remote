function submitLoginForm() {
    // get the email input value
    let email = document.getElementById("email_input").value;
    let code = document.getElementById("code_input").value

    headers = {};
    headers["email"] = email;

    if (code == "") {
        // 
    }

    // make a httpReq to the backend with the email in the headers
    httpReq(`/api/requestCode/code`, "POST", true, headers = headers)
        .then((response) => {
            console.log(response);
            // if the response is not null, show the code input
            if (response) {
                element = document.getElementById("code_input");

                // remove the hidden class
                element.removeAttribute("hidden");
            }
        });
}


code_input_box = document.getElementById("code_input")
// on keypress
code_input_box.onkeypress = function (e) {
    // check of the length of the value is 6
    if (code_input_box.value.length == 6) {
        // if it is, submit the form
        submitCodeForm();
    }
}