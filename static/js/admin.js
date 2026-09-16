/**
 * Admin Dashboard Helper Scripts
 */

document.addEventListener('DOMContentLoaded', function () {
  // Confirm deletion for dangerous actions
  const deleteForms = document.querySelectorAll('.confirm-delete-form');
  deleteForms.forEach(form => {
    form.addEventListener('submit', function (e) {
      const entity = form.getAttribute('data-entity') || 'item';
      if (!confirm(`Are you sure you want to permanently delete this ${entity}? This action cannot be undone.`)) {
        e.preventDefault();
      }
    });
  });
});
