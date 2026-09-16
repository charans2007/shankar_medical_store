/**
 * Medicare Medical Store - Product Catalogue Client-Side Filtering & Live Search
 */

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('productSearchInput');
  const productCards = document.querySelectorAll('.product-card');
  const emptyState = document.getElementById('productsEmptyState');
  const productCountDisplay = document.getElementById('productCountDisplay');

  if (!searchInput) return;

  let debounceTimer;

  // Real-time frontend instantaneous filtering
  searchInput.addEventListener('input', function (e) {
    clearTimeout(debounceTimer);
    const query = e.target.value.toLowerCase().trim();

    debounceTimer = setTimeout(() => {
      let visibleCount = 0;

      productCards.forEach(card => {
        const title = card.getAttribute('data-name') || '';
        const category = card.getAttribute('data-category') || '';
        const brand = card.getAttribute('data-brand') || '';
        const desc = card.getAttribute('data-desc') || '';

        const matches = (
          title.toLowerCase().includes(query) ||
          category.toLowerCase().includes(query) ||
          brand.toLowerCase().includes(query) ||
          desc.toLowerCase().includes(query)
        );

        if (matches) {
          card.style.display = 'flex';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      if (productCountDisplay) {
        productCountDisplay.textContent = visibleCount;
      }

      if (emptyState) {
        emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
      }
    }, 150);
  });
});
