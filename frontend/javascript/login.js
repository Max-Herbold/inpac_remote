// If the user is already logged in but they're 
// trying to access the login page, an existing
// session token is invalidated and the user is
// redirected to the login page.
logoutUser();

let timer = null;
const CODE_LENGTH = 8;

function submitLoginForm() {
    // get the email input value
    let code = document.getElementById("code_input").value

    if (code.length == CODE_LENGTH) {
        submitCodeForm();
    } else {
        // there is a in the box and doesnt have a length of CODE_LENGTH
        shakeBox("code_input");
        shakeBox("code_submit_button");
    }
}

function submitCodeForm() {
    const email_input_value = document.getElementById("email_input").value;
    const code_input = document.getElementById("code_input");
    const code_input_value = code_input.value;

    // reset the code input
    code_input.value = "";

    showById("code-form", false)
    showById("loader", true)

    // make a httpReq to the backend with the email and code in the headers
    headers = {};
    headers["email"] = email_input_value;
    headers["code"] = code_input_value;

    httpReq(`/api/code/verify`, "POST", true, headers = headers)
        .then((response) => {
            if (response) {
                // if the response is not null, show the success message
                showById("loader", false)
                submitCodeSuccess(response);
            } else {
                // if the response is null, show the error message
                submitCodeFailed(response);
            }
        }).catch((error) => {
            console.error(error);
            console.error(error.response);
            submitCodeFailed(error.response);
        });
}

function submitCodeSuccess(response) {
    // load the token into cookies
    addCookie("token", response.token);
    // redirect to the dashboard
    window.location.href = "/dashboard";
}

function submitCodeFailed(errorMessage) {
    showById("loader", false)
    showById("code-form", true)
    // show the error message
    document.getElementById("code_error_message").innerText = errorMessage;
}

function submitEmailForm() {
    // get the email input value
    let email = document.getElementById("email_input").value;

    // check if the email is valid
    if (email.length < 1) {
        shakeBox("email_input");
        shakeBox("email_submit_button");
    } else if (!email.includes("@") || !email.includes(".")) {
        shakeBox("email_input");
        shakeBox("email_submit_button");
    } else {
        requestCode(email);
    }
}

function requestCode(email) {
    showById("email-form", false)
    showById("code-form", false)
    showById("loader", true)

    document.getElementById("email_error_message").innerText = "";
    document.getElementById("code_error_message").innerText = "";

    headers = {};
    headers["email"] = email;

    // make a httpReq to the backend with the email in the headers
    httpReq(`/api/code/new`, "POST", true, headers = headers)
        .then((response) => {
            // if the response is not null, show the code input
            if (response) {
                codeSent();
            }
        }).catch((error) => {
            console.error(error);
            console.error(error.response);
            codeSentFailed(error.response);
        });
}

function codeSent() {
    showById("loader", false)
    showById("email-form", false)
    showById("code-form", true)

    // start a 1 second timer for 30 seconds
    let seconds = 30;
    const resendButton = document.getElementById("resend");
    // set the text to 30 seconds
    resendButton.innerText = "Resend code (30)";
    timer = setInterval(() => {
        seconds -= 1;
        resendButton.innerText = `Resend code (${seconds.toString().padStart(2, "0")})`;
        if (seconds <= 0) {
            clearInterval(timer);

            // enable the resend button
            resendButton.removeAttribute("disabled");
            resendButton.innerText = "Resend code";
        }
    }, 1000);

    // focus on the code input
    const code_id = document.getElementById("code_input");
    code_id.placeholder = `Code 00000000`;
    code_id.maxLength = CODE_LENGTH;
    code_id.focus();
}

function codeSentFailed(errorMessage) {
    // reset the form
    resetForm();
    // show the error message
    document.getElementById("email_error_message").innerText = errorMessage;
}

function resetForm() {
    showById("email-form", true)
    showById("loader", false)
    showById("code-form", false)
    document.getElementById("code_input").value = "";
    document.getElementById("email_error_message").innerText = "";
    document.getElementById("code_error_message").innerText = "";

    if (timer) {
        clearInterval(timer);
    }
}

function showById(id, show) {
    element = document.getElementById(id);
    if (element == null) {
        console.error(`Element with id ${id} not found`);
        return;
    }
    if (show) {
        element.removeAttribute("hidden");
        if (id == "code-form") {
            // focus on the code input
            const code_id = document.getElementById("code_input");
            code_id.focus();
        } else if (id == "email-form") {
            // focus on the email input
            const email_id = document.getElementById("email_input");
            email_id.focus();
        }
    } else {
        element.setAttribute("hidden", true);
    }
}

function shakeBox(id) {
    document.getElementById(id).classList.add("shake");
    setTimeout(() => {
        document.getElementById(id).classList.remove("shake");
    }, 300);
}

code_input_box = document.getElementById("code_input")
code_input_box.oninput = function (e) {
    error_message = document.getElementById("code_error_message");
    error_message.innerText = "";

    // check if any characters are not numbers
    if (code_input_box.value.match(/\D/)) {
        // if there are, remove them
        code_input_box.value = code_input_box.value.replace(/\D/g, '');
        shakeBox("code_input");
        shakeBox("code_submit_button");
    }

    if (e.keyCode == 13) {
        // enter pressed
        if (code_input_box.value.length != CODE_LENGTH) {
            shakeBox("code_input");
            shakeBox("code_submit_button");
        } else {
            submitCodeForm();
            return;
        }
    } else if (e.keyCode < 48 || e.keyCode > 57) {
        // check if a valid key (0-9) was pressed
        // if not, prevent the default action
        e.preventDefault();
        shakeBox("code_input");
        shakeBox("code_submit_button");
    } else if (code_input_box.value.length == CODE_LENGTH) {
        // submit the form
        submitCodeForm();
    }
}

document.getElementById("resend").addEventListener("click", function () {
    // disable the button
    this.setAttribute("disabled", true);
    // get the email input value
    let email = document.getElementById("email_input").value;
    requestCode(email);
});

window.addEventListener("load", function (event) {
    // focus on the email input
    document.getElementById("email_input").focus();

    // add event listener to the change button
    document.getElementById("change").addEventListener("click", function () {
        resetForm();
    });
});
