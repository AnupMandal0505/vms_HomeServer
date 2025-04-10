$(document).ready(function () {
    $('#userTable').DataTable();

    // Open Modal on "Add Passkey" Click
    $('.add-passkey-btn').click(function () {
        let userId = $(this).data('userid');
        $('#userId').val(userId);
        $('#passkeyInput').val('');  // Clear input field
        $('#errorMsg').addClass('d-none');  // Hide error message
        $('#passkeyModal').modal('show');
    });

    // Handle Form Submission
    $('#passkeyForm').submit(function (event) {
        event.preventDefault();
        let userId = $('#userId').val();
        let passKey = $('#passkeyInput').val();

        $.ajax({
            url: '/api/save-passkey/',  // API URL (adjust as needed)
            type: 'POST',
            data: { user_id: userId, pass_key: passKey },
            success: function (response) {
                if (response.success) {
                    // Update table and close modal
                    $(`button[data-userid="${userId}"]`).replaceWith(`<span class="pass-key">${passKey}</span>`);
                    $('#passkeyModal').modal('hide');
                } else {
                    $('#errorMsg').removeClass('d-none');  // Show error message
                }
            },
            error: function () {
                $('#errorMsg').removeClass('d-none');
            }
        });
    });
});
