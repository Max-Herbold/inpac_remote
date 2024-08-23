function logoutUser() {
    headers = {};
    let token = getCookie("token");
    if (token) {
        headers["token"] = token
        httpReq(`/api/user/logout`, "POST", true, headers = headers)

        removeCookie("token");
    }

    // check if the current page is the dashboard
    if (window.location.pathname != "/") {
        window.location.href = "/";
    }
}
