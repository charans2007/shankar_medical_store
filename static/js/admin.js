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

  // Mobile Sidebar Drawer Toggle
  const sidebarToggle = document.getElementById('adminSidebarToggle');
  const sidebarClose = document.getElementById('adminSidebarClose');
  const sidebar = document.querySelector('.admin-sidebar');
  const backdrop = document.getElementById('adminSidebarBackdrop');

  function openSidebar() {
    if (sidebar) sidebar.classList.add('sidebar-open');
    if (backdrop) backdrop.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    if (sidebar) sidebar.classList.remove('sidebar-open');
    if (backdrop) backdrop.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      openSidebar();
    });
  }

  if (sidebarClose) {
    sidebarClose.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      closeSidebar();
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', function () {
      closeSidebar();
    });
  }

  // Close sidebar on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sidebar && sidebar.classList.contains('sidebar-open')) {
      closeSidebar();
    }
  });
});
