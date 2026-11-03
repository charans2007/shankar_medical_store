/**
 * Medicare Medical Store - Main Frontend Scripts
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Menu Drawer Toggle
  const mobileToggle = document.getElementById('mobileMenuToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerOverlay = document.getElementById('drawerOverlay');
  const closeDrawerBtn = document.getElementById('closeDrawerBtn');

  function openDrawer() {
    if (mobileDrawer && drawerOverlay) {
      mobileDrawer.classList.add('open');
      drawerOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeDrawer() {
    if (mobileDrawer && drawerOverlay) {
      mobileDrawer.classList.remove('open');
      drawerOverlay.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  if (mobileToggle) mobileToggle.addEventListener('click', openDrawer);
  if (closeDrawerBtn) closeDrawerBtn.addEventListener('click', closeDrawer);
  if (drawerOverlay) drawerOverlay.addEventListener('click', closeDrawer);

  // 2. FAQ Accordion Behavior
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    if (questionBtn) {
      questionBtn.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        // Close other open items
        faqItems.forEach(otherItem => {
          if (otherItem !== item) {
            otherItem.classList.remove('active');
          }
        });

        // Toggle current
        if (isActive) {
          item.classList.remove('active');
        } else {
          item.classList.add('active');
        }
      });
    }
  });

  // 3. Flash Alert Auto-Dismissal
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }, 6000);
  });

  // 4. Store Hours & Call/WhatsApp Restrictions
  const storeClosedModal = document.getElementById('storeClosedModal');
  const closeStoreModalBtn = document.getElementById('closeStoreModalBtn');
  const storeModalDismissBtn = document.getElementById('storeModalDismissBtn');
  const storeModalTitle = document.getElementById('storeModalTitle');
  const storeModalDesc = document.querySelector('.store-modal-desc');

  function isStoreCurrentlyOpen() {
    // Check authoritative server rendered flag
    const serverOpenFlag = document.body.getAttribute('data-store-open');
    if (serverOpenFlag === 'false') {
      return false;
    }

    // Dynamic client-side clock check to handle active sessions crossing store closure
    try {
      const now = new Date();
      // Monday = 1, Saturday = 6, Sunday = 0
      const day = now.getDay();
      if (day === 0) {
        // Sunday is closed
        return false;
      }
      const hours = now.getHours();
      const minutes = now.getMinutes();
      const totalMinutes = hours * 60 + minutes;
      
      // Mon - Sat: 10:00 AM (600 mins) to 8:00 PM (1200 mins)
      const openMinutes = 10 * 60; // 10:00
      const closeMinutes = 20 * 60; // 20:00
      
      if (totalMinutes < openMinutes || totalMinutes >= closeMinutes) {
        return false;
      }
    } catch (err) {
      console.warn('Clock validation fallback to server state', err);
    }

    return serverOpenFlag === 'true';
  }

  function openStoreClosedModal(actionType) {
    if (!storeClosedModal) return;

    const storeHours = document.body.dataset.storeHours || '10:00 AM – 8:00 PM';
    if (storeModalTitle) {
      storeModalTitle.textContent = 'Phone Calls Available During Store Hours Only';
    }
    if (storeModalDesc) {
      storeModalDesc.textContent = 'Our counter phone lines are operated during store operating hours (' + storeHours + '). You can send us a message on WhatsApp and our team will attend to it!';
    }

    storeClosedModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function closeStoreClosedModal() {
    if (!storeClosedModal) return;
    storeClosedModal.style.display = 'none';
    document.body.style.overflow = '';
  }

  if (closeStoreModalBtn) closeStoreModalBtn.addEventListener('click', closeStoreClosedModal);
  if (storeModalDismissBtn) storeModalDismissBtn.addEventListener('click', closeStoreClosedModal);
  
  if (storeClosedModal) {
    storeClosedModal.addEventListener('click', function (e) {
      if (e.target === storeClosedModal) {
        closeStoreClosedModal();
      }
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && storeClosedModal && storeClosedModal.style.display === 'flex') {
      closeStoreClosedModal();
    }
  });

  // Global Link Interceptor for Phone Calls Only
  // WhatsApp messages can be sent for store and clinic inquiries
  document.addEventListener('click', function (e) {
    const callActionEl = e.target.closest('a[href^="tel:"], .bar-call, .action-card.call');

    if (!callActionEl) return;

    if (!isStoreCurrentlyOpen()) {
      e.preventDefault();
      e.stopPropagation();
      openStoreClosedModal('call');
    }
  }, true);
  // 5. Compact Anchored Profile Photo Popover (Not Full Screen)
  const profilePhotoModal = document.getElementById('profilePhotoModal');
  const closeProfilePhotoBtn = document.getElementById('closeProfilePhotoBtn');

  function openProfilePhotoModal() {
    if (profilePhotoModal) {
      profilePhotoModal.style.display = 'flex';
    }
  }

  function closeProfilePhotoModal() {
    if (profilePhotoModal) {
      profilePhotoModal.style.display = 'none';
    }
  }

  function toggleProfilePhotoModal() {
    if (!profilePhotoModal) return;
    if (profilePhotoModal.style.display === 'flex') {
      closeProfilePhotoModal();
    } else {
      openProfilePhotoModal();
    }
  }

  // Toggle popover when clicking the profile button in footer
  document.addEventListener('click', function (e) {
    const trigger = e.target.closest('#viewProfilePhotoBtn, .footer-user-credit');
    if (trigger) {
      e.preventDefault();
      e.stopPropagation();
      toggleProfilePhotoModal();
      return;
    }

    // Close when clicking outside the popover container
    if (profilePhotoModal && profilePhotoModal.style.display === 'flex') {
      if (!e.target.closest('.footer-user-credit-container')) {
        closeProfilePhotoModal();
      }
    }
  });

  // Close when clicking the close button
  if (closeProfilePhotoBtn) {
    closeProfilePhotoBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      closeProfilePhotoModal();
    });
  }

  // Close on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && profilePhotoModal && profilePhotoModal.style.display === 'flex') {
      closeProfilePhotoModal();
    }
  });

  // 6. Doctor Consultant Profile Photo Popovers (Consultation Page)
  function setupDoctorPopover(btnId, modalId, closeBtnId) {
    const modal = document.getElementById(modalId);
    const btn = document.getElementById(btnId);
    const closeBtn = document.getElementById(closeBtnId);
    if (!modal || !btn) return;

    function openModal() {
      modal.style.display = 'flex';
      const rect = btn.getBoundingClientRect();
      const spaceBelow = window.innerHeight - rect.bottom;
      const spaceAbove = rect.top;

      // Prefer displaying below when adequate room exists below
      if (spaceBelow >= 240 || spaceBelow >= spaceAbove) {
        modal.classList.add('popover-below');
      } else {
        modal.classList.remove('popover-below');
      }
    }

    function closeModal() {
      modal.style.display = 'none';
    }

    function toggleModal() {
      if (modal.style.display === 'flex') {
        closeModal();
      } else {
        openModal();
      }
    }

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      toggleModal();
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        closeModal();
      });
    }

    document.addEventListener('click', function (e) {
      if (modal.style.display === 'flex') {
        if (!e.target.closest('#' + modalId) && !e.target.closest('#' + btnId)) {
          closeModal();
        }
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.style.display === 'flex') {
        closeModal();
      }
    });
  }

  setupDoctorPopover('viewDoctorPhotoBtn', 'doctorPhotoModal', 'closeDoctorPhotoBtn');
  setupDoctorPopover('viewPhysicalDoctorPhotoBtn', 'physicalDoctorPhotoModal', 'closePhysicalDoctorPhotoBtn');
  setupDoctorPopover('viewFounderPhotoBtn', 'founderPhotoModal', 'closeFounderPhotoBtn');

});

