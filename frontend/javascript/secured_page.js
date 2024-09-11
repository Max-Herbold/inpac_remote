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
    document.body.innerHTML = `<div id="header-div"></div>${document.body.innerHTML}`;
    // document.getElementById("header-div").innerHTML = `<h1>Secured Page ${email}</h1>`;

    const headerDiv = document.getElementById("header-div");
    // make the header div show at the top of the page
    headerDiv.style.position = "fixed";
    headerDiv.style.width = "100%";
    headerDiv.style.backgroundColor = "black";
    headerDiv.style.color = "white";

    // headerDiv.style.marginLeft = "-1rem";
    // headerDiv.style.marginRight = "0";
    headerDiv.style.padding = "10px"
    headerDiv.style.textAlign = "center";

    headerDiv.style.zIndex = "100";
    headerDiv.style.top = "0";
    headerDiv.style.right = "0";
    headerDiv.style.left = "0";
    // ensure no other elements are hidden by the header
    document.body.style.marginTop = "110px";

    headerDiv.innerHTML = `
    <img src="/assets/images/inpac.png" style="position: fixed; display: block; height: 75px; width: 75px; left: 10px;"/>
    <h1>Secured Page ${email}</h1>
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