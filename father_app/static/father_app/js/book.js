document.addEventListener('DOMContentLoaded', function() {
    const leftPage = document.getElementById('left-page');
    const rightPage = document.getElementById('right-page');
    const prevBtn = document.getElementById('prev-spread');
    const nextBtn = document.getElementById('next-spread');
    const pageIndicator = document.getElementById('page-indicator');

    let currentLeftPage = 1;
    const totalPages = parseInt(document.getElementById('total-pages').value, 10);
    const pdfUrl = document.getElementById('pdf-url').value;

    function updateView() {
        const newRightPage = Math.min(currentLeftPage + 1, totalPages);

        leftPage.src = `${pdfUrl}#page=${currentLeftPage}&view=FitH`;
        rightPage.src = `${pdfUrl}#page=${newRightPage}&view=FitH`;

        pageIndicator.textContent = `Страницы ${currentLeftPage}-${newRightPage}`;

        prevBtn.disabled = currentLeftPage <= 1;
        nextBtn.disabled = newRightPage >= totalPages;
    }

    prevBtn.addEventListener('click', function() {
        if (currentLeftPage > 1) {
            currentLeftPage = Math.max(1, currentLeftPage - 2);
            updateView();
        }
    });

    nextBtn.addEventListener('click', function() {
        if (currentLeftPage + 1 < totalPages) {
            currentLeftPage += 2;
            updateView();
        }
    });

    updateView();
});
