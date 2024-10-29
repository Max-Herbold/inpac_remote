window.addEventListener('load', () => {
    // validate the token
    const token = getCookie("token");
    if (!token) {
        window.location.href = "/debug_login";
    }

    httpReq(`/api/user/email`, "GET", true)
        .then((response) => {
        }).catch((error) => {
            window.location.href = "/debug_login";
        });
});