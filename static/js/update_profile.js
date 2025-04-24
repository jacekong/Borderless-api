import Toast from './toast.js';

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("update_profile_form");
    const submitButton = document.getElementById("submit-profile-form");
    const avatarInput = document.getElementById("upload_profile_avatar");

    let avatar = null;

    if (avatarInput) {
        avatarInput.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (file) {
                avatar = file;
                const reader = new FileReader();
                reader.onload = function (e) {
                    const previewImage = document.getElementById("avatar_preview");
                    previewImage.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
    
            submitButton.disabled = true;
    
            // get form data
            const bio = document.querySelector("#bio").value;
            const userName = document.querySelector("#name").value;
            
            // Perform the AJAX request
            const formData = new FormData(form);
            if (bio) {
                formData.append("bio", bio);
            }
            if (userName) {
                formData.append("name", userName);
            }
            if (avatar) {
                formData.append("avatar", avatar);
            }
    
            fetch(form.action, {
                method: "PUT",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === "success") {
                    Toast.message("Profile updated successfully!");
                    window.location.replace(data.redirect_url);
                } else {
                    console.log("Error:", data);
                    
                    Toast.error("Something went wrong")
                }
            })
            .catch(error => {
                console.error("Error:", error);
                Toast.error("Something went wrong")
            })
            .finally(() => {
                submitButton.disabled = false;
            });
        });
    }

});