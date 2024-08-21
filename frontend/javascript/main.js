function submitLoginForm() {
    // get the email input value
    let email = document.getElementById('email_input').value;
    console.log(email);

    headers = {};
    headers['email'] = email;

    // make a httpReq to the backend with the email in the headers
    httpReq(`/api/requestCode/code`, "POST", true, headers = headers)
        .then((response) => {
            console.log(response);
            // if the response is not null, show the code input
            if (response) {
                element = document.getElementById('code_input');

                // remove the hidden class
                element.classList.remove('hidden');
            }
        });
}
