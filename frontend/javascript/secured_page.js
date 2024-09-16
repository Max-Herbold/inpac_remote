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

// add header to body
function addHeader(email) {
    // always include the header css with the header itself
    const link = document.createElement("link");
    link.href = "/css/header.css";
    link.rel = "stylesheet";
    document.head.appendChild(link);

    // add the header div to the body
    document.body.innerHTML = `<div id="header-div"></div>${document.body.innerHTML}`;

    // add the header to the header div
    const headerDiv = document.getElementById("header-div");
    headerDiv.innerHTML = `
    <img src="/assets/images/inpac.png" id="header-image"/>
    <h1>placeholder</h1>
    <div>
        <button id="logoutButton" onclick="logoutUser()">Logout</button>
    </div>
    `;
}

window.addEventListener('load', () => {
    // validate the token
    const token = getCookie("token");
    if (!token) {
        window.location.href = "/";
    }

    httpReq(`/api/user/email`, "GET", true)
        .then((response) => {
            if (response) {
                let email = response.email;
                displayLoggedInUser(email);
                addHeader(email);
            }
        }).catch((error) => {
            window.location.href = "/";
        });
});