// Main interactive JavaScript for Vibe Guestbook

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-dismiss toasts after 4 seconds
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-8px)';
            setTimeout(() => toast.remove(), 400);
        }, 4000);
    });

    // 2. Real-time Search & Filter on the messages feed
    const searchInput = document.getElementById('search-input');
    const entryCards = document.querySelectorAll('.entry-card');
    const emptyState = document.getElementById('search-empty-state');
    const entriesList = document.querySelector('.entries-grid');

    if (searchInput && entryCards.length > 0) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            let visibleCount = 0;

            entryCards.forEach(card => {
                const name = card.getAttribute('data-name')?.toLowerCase() || '';
                const message = card.getAttribute('data-message')?.toLowerCase() || '';

                if (name.includes(query) || message.includes(query)) {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            if (emptyState) {
                if (visibleCount === 0) {
                    emptyState.style.display = 'block';
                } else {
                    emptyState.style.display = 'none';
                }
            }
        });
    }

    // 3. Live Character Counter for form
    const messageInput = document.getElementById('message');
    const charCounter = document.getElementById('char-count');
    if (messageInput && charCounter) {
        const updateCount = () => {
            charCounter.textContent = messageInput.value.length;
        };
        messageInput.addEventListener('input', updateCount);
        updateCount();
    }

    // 4. Modal Dialog for Delete Confirmation
    const deleteDialog = document.getElementById('delete-dialog');
    const confirmDeleteForm = document.getElementById('confirm-delete-form');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
    const deleteButtons = document.querySelectorAll('.btn-trigger-delete');

    if (deleteDialog && confirmDeleteForm) {
        deleteButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const deleteUrl = btn.getAttribute('data-url');
                const authorName = btn.getAttribute('data-author');

                confirmDeleteForm.action = deleteUrl;
                const authorPlaceholder = document.getElementById('delete-author-name');
                if (authorPlaceholder) {
                    authorPlaceholder.textContent = authorName || 'lời nhắn này';
                }

                if (typeof deleteDialog.showModal === 'function') {
                    deleteDialog.showModal();
                } else {
                    if (confirm(`Bạn có chắc muốn xóa lời nhắn của ${authorName}?`)) {
                        confirmDeleteForm.submit();
                    }
                }
            });
        });

        if (cancelDeleteBtn) {
            cancelDeleteBtn.addEventListener('click', () => {
                deleteDialog.close();
            });
        }

        // Close on backdrop click
        deleteDialog.addEventListener('click', (e) => {
            const rect = deleteDialog.getBoundingClientRect();
            const isInDialog = (rect.top <= e.clientY && e.clientY <= rect.top + rect.height
                && rect.left <= e.clientX && e.clientX <= rect.left + rect.width);
            if (!isInDialog) {
                deleteDialog.close();
            }
        });
    }
});
