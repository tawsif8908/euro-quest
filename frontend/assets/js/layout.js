
// Load Navbar + Footer automatically
document.addEventListener("DOMContentLoaded", () => {

    // Navbar inject
    fetch("components/navbar.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("navbar").innerHTML = data;
        });

    // Footer inject
    fetch("components/footer.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("footer").innerHTML = data;
        });
});
