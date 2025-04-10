document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent default form submission

            const email = document.getElementById("identifier").value;
            const password = document.getElementById("password").value;

            const response = await fetch("http://127.0.0.1:8000/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // Redirect or show success message
                alert("Login successful!");
                window.location.href = "/dashboard/"; // Redirect to dashboard
            } else {
                // Show error message
                alert(data.error || "Login failed. Please try again.");
            }
        });
    }
});
