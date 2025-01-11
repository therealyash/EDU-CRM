document.addEventListener('DOMContentLoaded', function() {
    // Rich Text Editor
    const editor = document.getElementById('editor');
    const message = document.getElementById('message');
    const form = document.getElementById('emailForm');

    // Update hidden textarea before form submission
    form.addEventListener('submit', function() {
        message.value = editor.innerHTML;
    });

    // Toolbar functionality
    document.querySelectorAll('.toolbar-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const command = this.dataset.command;
            if (command === 'createLink') {
                const url = prompt('Enter the URL:');
                if (url) document.execCommand(command, false, url);
            } else {
                document.execCommand(command, false, null);
            }
            editor.focus();
        });
    });

    // Image Upload Preview
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const uploadPlaceholder = document.getElementById('uploadPlaceholder');
    const removeImage = document.getElementById('removeImage');

    imageInput.addEventListener('change', function(e) {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImg.src = e.target.result;
                imagePreview.style.display = 'block';
                uploadPlaceholder.style.display = 'none';
            }
            reader.readAsDataURL(file);
        }
    });

    removeImage.addEventListener('click', function() {
        imageInput.value = '';
        imagePreview.style.display = 'none';
        uploadPlaceholder.style.display = 'block';
    });

    // Recipients Selection
    const selectAll = document.getElementById('selectAll');
    const clearAll = document.getElementById('clearAll');
    const checkboxes = document.querySelectorAll('input[name="recipients"]');

    selectAll.addEventListener('click', function() {
        checkboxes.forEach(checkbox => checkbox.checked = true);
    });

    clearAll.addEventListener('click', function() {
        checkboxes.forEach(checkbox => checkbox.checked = false);
    });

    // Save as Draft functionality
    document.getElementById('saveAsDraft').addEventListener('click', function() {
        // Implement draft saving logic here
        alert('Draft saved successfully!');
    });
});
    document.getElementById('emailForm').addEventListener('submit', function(e) {
        // Get content from editor and set it to hidden textarea
        const editorContent = document.getElementById('editor').innerHTML;
        document.getElementById('message').value = editorContent;
    });