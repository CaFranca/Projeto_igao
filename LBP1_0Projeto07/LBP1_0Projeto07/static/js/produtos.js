let currentSlide = 0; // Controla o índice do produto atual
const totalProducts = document.querySelectorAll('.product-card').length; // Número total de produtos
const productsToShow = 4; // Número de produtos a serem exibidos por vez
const carousel = document.getElementById('productCarousel'); // O grid do carrossel

// Função para atualizar a visibilidade dos produtos
function updateProductVisibility() {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        if (index >= currentSlide && index < currentSlide + productsToShow) {
            card.style.display = 'block'; // Mostra os produtos que estão na faixa atual
        } else {
            card.style.display = 'none'; // Esconde os demais produtos
        }
    });
}

// Função para mover o carrossel
function moveSlide(direction) {
    // Atualiza o índice do slide com base na direção
    currentSlide += direction;
    
    // Garante que o carrossel não ultrapasse os limites de produtos
    if (currentSlide < 0) {
        currentSlide = 0; // Se está na primeira slide, não deixa ir para trás
    } else if (currentSlide > totalProducts - productsToShow) {
        currentSlide = totalProducts - productsToShow; // Se está no último grupo, não deixa ir além
    }
    
    // Atualiza a visibilidade dos produtos
    updateProductVisibility();

    // Move o carrossel aplicando uma transformação baseada no índice e na largura dos produtos
    carousel.style.transform = `translateX(${-currentSlide * productWidth}px)`;
}

// Inicializa a visibilidade dos produtos ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    updateProductVisibility(); // Chama a função para mostrar os produtos iniciais
});
