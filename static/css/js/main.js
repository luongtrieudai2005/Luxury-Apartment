document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('sidebarToggle');
  const wrapper = document.getElementById('wrapper');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      wrapper.classList.toggle('toggled');
    });
  }
});
