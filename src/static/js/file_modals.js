function openImageModal(imageSrc, filename) {
    document.getElementById('modalImage').src = imageSrc;
    document.getElementById('imageModalLabel').textContent = filename || 'Resource Preview';
    new bootstrap.Modal(document.getElementById('imageModal')).show();
}

function openSubmissionImageModal(imageSrc, filename) {
    document.getElementById('modalSubmissionImage').src = imageSrc;
    document.getElementById('submissionImageModalLabel').textContent = filename || 'Submission Preview';
    new bootstrap.Modal(document.getElementById('submissionImageModal')).show();
}

function openTeacherImageModal(imageSrc, filename) {
    document.getElementById('modalTeacherImage').src = imageSrc;
    document.getElementById('teacherImageModalLabel').textContent = filename || 'Submission Preview';
    new bootstrap.Modal(document.getElementById('teacherImageModal')).show();
}
