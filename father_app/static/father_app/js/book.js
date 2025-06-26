document.addEventListener('DOMContentLoaded', function() {
    const leftPage = document.getElementById('left-page');
    const rightPage = document.getElementById('right-page');
    const prevBtn = document.getElementById('prev-spread');
    const nextBtn = document.getElementById('next-spread');
    const pageIndicator = document.getElementById('page-indicator');
    const leftLoading = document.getElementById('left-loading');
    const rightLoading = document.getElementById('right-loading');

    let currentLeftPage = 1;
    const totalPages = parseInt(document.getElementById('total-pages').value, 10);
    const pdfUrl = document.getElementById('pdf-url').value;

    // ОТЛАДКА: Выводим информацию в консоль
    console.log('=== PDF VIEWER DEBUG ===');
    console.log('PDF URL:', pdfUrl);
    console.log('Total pages:', totalPages);
    console.log('Left page element:', leftPage);
    console.log('Right page element:', rightPage);

    // Проверяем, есть ли PDF URL
    if (!pdfUrl || pdfUrl === 'None' || pdfUrl === '' || pdfUrl === 'null') {
        console.error('❌ PDF URL не найден или пустой');
        if (leftLoading) leftLoading.innerHTML = '❌ PDF файл не найден';
        if (rightLoading) rightLoading.innerHTML = '❌ PDF файл не найден';
        return;
    }

    // Проверяем доступность PDF файла
    fetch(pdfUrl, { method: 'HEAD' })
        .then(response => {
            console.log('PDF файл доступен:', response.ok, response.status);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
        })
        .catch(error => {
            console.error('❌ Ошибка доступа к PDF файлу:', error);
            if (leftLoading) leftLoading.innerHTML = '❌ PDF файл недоступен';
            if (rightLoading) rightLoading.innerHTML = '❌ PDF файл недоступен';
        });

    // Функция для скрытия индикатора загрузки
    function hideLoading(side) {
        if (side === 'left' && leftLoading) {
            leftLoading.style.display = 'none';
        } else if (side === 'right' && rightLoading) {
            rightLoading.style.display = 'none';
        }
    }

    // Функция для показа индикатора загрузки
    function showLoading(side, message = 'Загрузка...') {
        if (side === 'left' && leftLoading) {
            leftLoading.style.display = 'block';
            leftLoading.innerHTML = message;
        } else if (side === 'right' && rightLoading) {
            rightLoading.style.display = 'block';
            rightLoading.innerHTML = message;
        }
    }

    // Обработчики загрузки iframe
    leftPage.addEventListener('load', function() {
        console.log('✅ Левая страница загружена');
        hideLoading('left');
    });

    rightPage.addEventListener('load', function() {
        console.log('✅ Правая страница загружена');
        hideLoading('right');
    });

    // Обработчики ошибок
    leftPage.addEventListener('error', function(e) {
        console.error('❌ Ошибка загрузки левой страницы:', e);
        showLoading('left', '❌ Ошибка загрузки');
    });

    rightPage.addEventListener('error', function(e) {
        console.error('❌ Ошибка загрузки правой страницы:', e);
        showLoading('right', '❌ Ошибка загрузки');
    });

    function updateView() {
        const newRightPage = Math.min(currentLeftPage + 1, totalPages);

        console.log(`📖 Обновление просмотра: страницы ${currentLeftPage}-${newRightPage}`);

        // Показываем индикаторы загрузки
        showLoading('left', 'Загрузка левой страницы...');
        showLoading('right', 'Загрузка правой страницы...');

        // Пробуем разные методы отображения PDF

        // Метод 1: Прямой URL с параметром page
        const leftUrl = `${pdfUrl}#page=${currentLeftPage}`;
        const rightUrl = `${pdfUrl}#page=${newRightPage}`;

        console.log('📄 Left URL:', leftUrl);
        console.log('📄 Right URL:', rightUrl);

        leftPage.src = leftUrl;
        rightPage.src = rightUrl;

        // Обновляем индикатор страниц
        if (currentLeftPage === newRightPage) {
            pageIndicator.textContent = `Страница ${currentLeftPage} из ${totalPages}`;
        } else {
            pageIndicator.textContent = `Страницы ${currentLeftPage}-${newRightPage} из ${totalPages}`;
        }

        // Управление кнопками навигации
        prevBtn.disabled = currentLeftPage <= 1;
        nextBtn.disabled = newRightPage >= totalPages;
    }

    // Альтернативный метод отображения PDF
    function tryAlternativeMethod() {
        console.log('🔄 Пробуем альтернативный метод отображения...');

        // Метод 2: Использование PDF.js viewer
        const viewerUrl = '/static/pdfjs/web/viewer.html';
        const leftUrl = `${viewerUrl}?file=${encodeURIComponent(pdfUrl)}#page=${currentLeftPage}`;
        const rightUrl = `${viewerUrl}?file=${encodeURIComponent(pdfUrl)}#page=${Math.min(currentLeftPage + 1, totalPages)}`;

        leftPage.src = leftUrl;
        rightPage.src = rightUrl;
    }

    // Обработчик кнопки "Назад"
    prevBtn.addEventListener('click', function() {
        if (currentLeftPage > 1) {
            currentLeftPage = Math.max(1, currentLeftPage - 2);
            updateView();
        }
    });

    // Обработчик кнопки "Вперёд"
    nextBtn.addEventListener('click', function() {
        if (currentLeftPage + 1 < totalPages) {
            currentLeftPage = Math.min(totalPages - 1, currentLeftPage + 2);
            updateView();
        }
    });

    // Обработка клавиатуры
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            e.preventDefault();
            prevBtn.click();
        } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            e.preventDefault();
            nextBtn.click();
        } else if (e.key === 'f' || e.key === 'F') {
            if (document.fullscreenElement) {
                document.exitFullscreen();
            } else {
                document.querySelector('.pdf-section').requestFullscreen();
            }
        }
    });

    // Инициализация
    updateView();

    // Проверка через 3 секунды
    setTimeout(function() {
        const leftSrc = leftPage.src;
        const rightSrc = rightPage.src;

        console.log('🔍 Проверка через 3 секунды:');
        console.log('Left iframe src:', leftSrc);
        console.log('Right iframe src:', rightSrc);

        if (!leftSrc || !rightSrc || leftSrc === 'about:blank' || rightSrc === 'about:blank') {
            console.log('⚠️ PDF не загрузился, пробуем альтернативный метод...');
            tryAlternativeMethod();
        }
    }, 3000);

    // Финальная проверка через 10 секунд
    setTimeout(function() {
        if (leftLoading && leftLoading.style.display !== 'none') {
            console.log('❌ PDF так и не загрузился');
            showLoading('left', '❌ Не удалось загрузить PDF.<br><a href="' + pdfUrl + '" target="_blank">Открыть напрямую</a>');
        }
        if (rightLoading && rightLoading.style.display !== 'none') {
            showLoading('right', '❌ Не удалось загрузить PDF.<br><a href="' + pdfUrl + '" target="_blank">Открыть напрямую</a>');
        }
    }, 10000);
});