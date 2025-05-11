console.log("JavaScript is connected!");

document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", () => {
            alert("Form submitted!");
        });
    }
});
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
