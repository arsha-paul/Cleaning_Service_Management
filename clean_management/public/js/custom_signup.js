$(document).ready(function() {
    let params = new URLSearchParams(window.location.search);
    if (params.get("redirect-to") === "/app/home") {
        window.location.href = "/login#signup";
    }
});
