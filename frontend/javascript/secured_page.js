window.addEventListener('beforeunload', () => {
    // create a button that redirects '/'
    const buttonHtml = `<p>Invalid redirect. Please refresh the page.</p>
    <button onclick="window.location.reload()">Refresh</button>
    <button onclick="window.location.href='/'">Back to login</button>`;
    document.body.innerHTML = buttonHtml;
    window.location.reload();
});

// make this a header bar
function displayLoggedInUser(email) {
    if (email) {
        const string = `Logged in as ${email}`;
        document.getElementById("test-validator").innerHTML = string;
    } else {
        window.location.href = "/";
    }
}

window.addEventListener('load', () => {
    // validate the token
    const token = getCookie("token");
    if (!token) {
        window.location.href = "/";
    }

    httpReq(`/api/user/email`, "GET", true, headers = { "token": token })
        .then((response) => {
            if (response) {
                let email = response.email;
                displayLoggedInUser(email);
            }
        }).catch((error) => {
            window.location.href = "/";
        });
});