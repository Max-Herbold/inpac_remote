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
        const string = `${email}`;
        try {
            document.getElementById("loggedInAsDisplay").innerHTML = string;
        } catch (error) {
            console.error(error);
        }
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
    <div>
        <a href="/dashboard">
            <img src="/assets/images/inpac.png" id="header-image"/>
        </a>
        <h1 id=headerText>Dashboard</h1>
    </div>
    <div id="logOutButtonDiv">
        <p id="loggedInAsDisplayParagraph">
            <span>Logged in as: </span>
            <span id=loggedInAsDisplay></span>
        </p>
        <button id="logoutButton" onclick="logoutUser()">Logout</button>
    </div>
    `;
}

function setHeaderText(text) {
    const headerText = document.getElementById("headerText");
    headerText.innerHTML = text;
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
                addHeader(email);
                displayLoggedInUser(email);
            }
        }).catch((error) => {
            window.location.href = "/";
        });
});