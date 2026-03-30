// Drag-drop upload for admin/upload.html
(function () {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const filePreview = document.getElementById('file-preview');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const fileRemove = document.getElementById('file-remove');
    const submitBtn = document.getElementById('submit-btn');
    const dropIcon = document.getElementById('drop-icon');
    const dropText = document.getElementById('drop-text');

    if (!dropZone || !fileInput) return;

    // Click to select
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag events
    ['dragenter', 'dragover'].forEach(evt => {
        dropZone.addEventListener(evt, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('drop-zone-active');
        });
    });

    ['dragleave', 'drop'].forEach(evt => {
        dropZone.addEventListener(evt, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('drop-zone-active');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFile(fileInput.files[0]);
        }
    });

    function handleFile(file) {
        // Validate extension
        const ext = file.name.toLowerCase().split('.').pop();
        if (ext !== 'html' && ext !== 'htm') {
            alert('Hanya file .html atau .htm yang diperbolehkan.');
            return;
        }

        // Validate size (10 MB)
        if (file.size > 10 * 1024 * 1024) {
            alert('Ukuran file melebihi 10 MB.');
            return;
        }

        // Update file input
        const dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;

        // Show preview
        fileName.textContent = file.name;
        fileSize.textContent = formatSize(file.size);
        filePreview.classList.remove('hidden');
        dropIcon.textContent = '✅';
        dropText.textContent = file.name;
        submitBtn.disabled = false;
    }

    // Remove file
    if (fileRemove) {
        fileRemove.addEventListener('click', () => {
            fileInput.value = '';
            filePreview.classList.add('hidden');
            dropIcon.textContent = '📄';
            dropText.textContent = 'Drag & drop file HTML di sini';
            submitBtn.disabled = true;
        });
    }

    function formatSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
})();
