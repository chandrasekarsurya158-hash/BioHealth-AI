/**
 * Multi-Domain AI Disease Detection & Intelligent Health Assistance
 * Interactive Client-Side JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. File Upload Preview & Drag-and-Drop Handler
    const fileInput = document.getElementById('fileInput');
    const uploadZone = document.getElementById('uploadZone');
    const uploadPrompt = document.getElementById('uploadPrompt');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    const removeFileBtn = document.getElementById('removeFileBtn');

    if (fileInput && uploadZone) {
        // Drag over / leave effects
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });

        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragover');
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
            if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                handleFileSelection(fileInput.files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files && fileInput.files.length > 0) {
                handleFileSelection(fileInput.files[0]);
            }
        });

        if (removeFileBtn) {
            removeFileBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                fileInput.value = '';
                if (imagePreview) imagePreview.src = '#';
                imagePreviewContainer.classList.add('d-none');
                uploadPrompt.classList.remove('d-none');
            });
        }
    }

    function handleFileSelection(file) {
        // Maximum allowed file size: 16 MB
        const maxBytes = 16 * 1024 * 1024;
        if (file.size > maxBytes) {
            alert('File exceeds maximum allowed upload size of 16 MB. Please choose a smaller file.');
            fileInput.value = '';
            return;
        }

        if (fileNameDisplay) {
            fileNameDisplay.textContent = `${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
        }

        if (file.type.startsWith('image/') && imagePreview) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }

        if (uploadPrompt && imagePreviewContainer) {
            uploadPrompt.classList.add('d-none');
            imagePreviewContainer.classList.remove('d-none');
        }
    }

    // 2. Loading Spinner Trigger for AI Processing Forms
    const loadingForms = document.querySelectorAll('form.needs-loading');
    const loadingModalEl = document.getElementById('loadingModal');

    if (loadingForms.length > 0 && loadingModalEl) {
        const loadingModal = new bootstrap.Modal(loadingModalEl);
        loadingForms.forEach(form => {
            form.addEventListener('submit', () => {
                loadingModal.show();
            });
        });
    }
});
