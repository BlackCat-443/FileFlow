document.addEventListener("DOMContentLoaded", () => {
    const uploadButton = document.getElementById("uploadButton");
    const fileInput = document.getElementById("fileInput");
    const progressWrapper = document.getElementById("progressWrapper");
    const progressList = document.getElementById("progressList");

    const uploads = {}; // Track ongoing uploads

    uploadButton.addEventListener("click", (event) => {
        event.preventDefault(); // Mencegah form ter-submit secara default
        const files = fileInput.files;
        if (!files.length) {
            alert("Please select at least one file to upload.");
            return;
        }

        progressWrapper.style.display = "block";
        progressList.innerHTML = ""; // Reset daftar progres

        Array.from(files).forEach((file, index) => {
            // Tambahkan item ke progress list
            const listItem = document.createElement("li");
            listItem.className = "list-group-item";
            listItem.innerHTML = `
                <span>${file.name}</span>
                <div class="progress-bar-container">
                    <div class="progress-bar" id="progress-${index}"></div>
                </div>
            `;
            progressList.appendChild(listItem);

            // Mulai unggahan file
            const formData = new FormData();
            formData.append("files[]", file);

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/upload", true);

            // Perbarui progres bar berdasarkan progress event
            xhr.upload.addEventListener("progress", (event) => {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total) * 100;
                    const progressBar = document.getElementById(`progress-${index}`);
                    progressBar.style.width = `${percentComplete}%`;
                }
            });

            // Tampilkan status setelah unggahan selesai
            xhr.onload = () => {
                if (xhr.status === 200) {
                    const progressBar = document.getElementById(`progress-${index}`);
                    progressBar.style.backgroundColor = "#28a745"; // Hijau saat selesai
                } else {
                    alert(`Failed to upload ${file.name}`);
                }
            };

            xhr.onerror = () => {
                alert(`An error occurred while uploading ${file.name}`);
            };

            xhr.send(formData);
        });

        // Cancel button functionality
        progressList.addEventListener("click", (event) => {
            if (event.target.classList.contains("cancel-btn")) {
                const index = event.target.getAttribute("data-index");
                if (uploads[index]) {
                    uploads[index].abort(); // Cancel the request
                    delete uploads[index];

                    // Remove the file from UI
                    const listItem = event.target.closest("li");
                    listItem.remove();

                    // Remove the file from the input element
                    const filesArray = Array.from(fileInput.files);
                    filesArray.splice(index, 1); // Remove the canceled file
                    fileInput.files = new FileList(filesArray); // Update fileInput with the remaining files
                }
            }
        });
    });
});


// Handle success or error messages for login and registration

document.addEventListener("DOMContentLoaded", () => {
    const message = document.getElementById("message");

    // Success message for successful login
    if (message && message.dataset.success === "true") {
        Swal.fire({
            title: 'Success!',
            text: 'You have successfully logged in.',
            icon: 'success',
            confirmButtonText: 'OK'
        });
    }

    // Error handling for incorrect credentials
    if (message && message.dataset.success === "false") {
        Swal.fire({
            title: 'Error!',
            text: 'Invalid email or password.',
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }

    // Success message for successful registration
    if (message && message.dataset.register === "true") {
        Swal.fire({
            title: 'Success!',
            text: 'Your account has been successfully created.',
            icon: 'success',
            confirmButtonText: 'OK'
        });
    }

    // Error handling for registration issues
    if (message && message.dataset.register === "false") {
        Swal.fire({
            title: 'Error!',
            text: 'Something went wrong. Please try again.',
            icon: 'error',
            confirmButtonText: 'OK'
        });
    }
});




