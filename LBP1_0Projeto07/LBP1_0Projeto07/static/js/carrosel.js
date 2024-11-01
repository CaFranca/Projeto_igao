let currentIndex = 0;
        
function moveSlide(direction) {
    const productGrid = document.querySelector('.product-grid');
    const totalProducts = {{ produtos | length }};
    const itemsPerView = 3; // Número de produtos visíveis por vez
    const maxIndex = Math.ceil(totalProducts / itemsPerView) - 1; // Máximo de índices

    currentIndex += direction;

    // Restringe o índice entre 0 e o máximo
    if (currentIndex < 0) {
        currentIndex = 0;
    } else if (currentIndex > maxIndex) {
        currentIndex = maxIndex;
    }

    // Move o grid para a posição correta
    const offset = currentIndex * (100 / itemsPerView); // Cálculo do offset
    productGrid.style.transform = `translateX(-${offset}%)`;
}

// Adiciona listeners aos botões de navegação
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.prev').addEventListener('click', () => moveSlide(-1));
    document.querySelector('.next').addEventListener('click', () => moveSlide(1));
});