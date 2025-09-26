function enableCopyButtons(selector = '[data-copy]') {
    document.querySelectorAll(selector).forEach(el => {
        el.addEventListener('click', function (e) {
            e.preventDefault();

            const textToCopy = this.getAttribute('data-copy');
            if (!textToCopy) return;

            navigator.clipboard.writeText(textToCopy)
                .then(() => {
                    console.log(`Copied: ${textToCopy}`);
                    showToast('success', 'Success', 'Copied to clipboard!')
                })
                .catch(err => {
                    showToast('error', 'Error', 'Failed to copy.')
                });
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    enableCopyButtons();
});