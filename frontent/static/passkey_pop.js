$(document).ready(function () {
    // Show passkey modal when button is clicked
    $(".add-passkey-btn").click(function () {
        let userId = $(this).data("userid");
        $("#userId").val(userId);
        $("#passkeyInput").val("");
        $("#errorMsg").hide();
        $("#passkeyModal").modal("show");
    });

    // Prevent manual keydown input in passkey input field
    $("#passkeyInput").on("keydown", function (e) {
        e.preventDefault();
    });

    // Allow paste but handle it manually
    $("#passkeyInput").on("paste", function (e) {
        e.preventDefault();
        var clipboardData = e.originalEvent.clipboardData || window.clipboardData;
        var pastedText = clipboardData.getData("text");
        $(this).val(pastedText);
    });

    // Handle passkey form submission via AJAX
    $("#passkeyForm").submit(function (event) {
        event.preventDefault();
        let userId = $("#userId").val();
        let passKey = $("#passkeyInput").val();

        $.ajax({
            url: '/api/save-passkey/',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify({ user_id: userId, pass_key: passKey }),
            success: function (response) {
                if (response.success) {
                    $(`button[data-userid="${userId}"]`).replaceWith(`<span class="pass-key">${passKey}</span>`);
                    $("#passkeyModal").modal("hide");
                } else {
                    $("#errorMsg").show();
                }
            },
            error: function () {
                $("#errorMsg").show();
            }
        });
    });
});
