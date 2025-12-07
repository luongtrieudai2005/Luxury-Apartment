// // document.addEventListener('DOMContentLoaded', function () {
// //   const toggleBtn = document.getElementById('sidebarToggle');
// //   const wrapper = document.getElementById('wrapper');
// //   if (toggleBtn) {
// //     toggleBtn.addEventListener('click', function () {
// //       wrapper.classList.toggle('toggled');
// //     });
// //   }
// // });

// // document.addEventListener("DOMContentLoaded", () => {
// //   const wrapper = document.getElementById("wrapper");
// //   const btn = document.getElementById("sidebarToggle");
// //   const backdrop = document.getElementById("sidebarBackdrop");

// //   if (!wrapper || !btn) return;

// //   const setOpen = (open) => {
// //     wrapper.classList.toggle("sidebar-open", open);
// //     if (backdrop) backdrop.classList.toggle("show", open);
// //     btn.setAttribute("aria-expanded", open ? "true" : "false");
// //   };

// //   const toggle = () => setOpen(!wrapper.classList.contains("sidebar-open"));

// //   btn.addEventListener("click", (e) => {
// //     e.preventDefault();
// //     toggle(); // ✅ nhấn lần 1 mở, lần 2 đóng
// //   });

// //   // click ra ngoài để đóng (optional nhưng nên có)
// //   if (backdrop) {
// //     backdrop.addEventListener("click", () => setOpen(false));
// //   }

// //   // nhấn ESC để đóng
// //   window.addEventListener("keydown", (e) => {
// //     if (e.key === "Escape") setOpen(false);
// //   });
// // });


// document.addEventListener("DOMContentLoaded", () => {
//   const wrapper = document.getElementById("wrapper");
//   const btn = document.getElementById("sidebarToggle");
//   const backdrop = document.getElementById("sidebarBackdrop");
//   if (!wrapper || !btn) return;

//   const isMobile = () => window.matchMedia("(max-width: 768px)").matches;

//   const syncBackdrop = () => {
//     if (!backdrop) return;
//     const open = wrapper.classList.contains("toggled");
//     // backdrop chỉ dùng cho mobile
//     backdrop.classList.toggle("show", open && isMobile());
//   };

//   btn.addEventListener("click", (e) => {
//     e.preventDefault();
//     wrapper.classList.toggle("toggled");
//     syncBackdrop();
//   });

//   if (backdrop) {
//     backdrop.addEventListener("click", () => {
//       wrapper.classList.remove("toggled");
//       syncBackdrop();
//     });
//   }

//   window.addEventListener("keydown", (e) => {
//     if (e.key === "Escape") {
//       wrapper.classList.remove("toggled");
//       syncBackdrop();
//     }
//   });

//   window.addEventListener("resize", syncBackdrop);
// });


document.addEventListener("DOMContentLoaded", () => {
  const wrapper = document.getElementById("wrapper");
  const btn = document.getElementById("sidebarToggle");
  const backdrop = document.getElementById("sidebarBackdrop");
  if (!wrapper || !btn) return;

  const isMobile = () => window.matchMedia("(max-width: 768px)").matches;

  const syncBackdrop = () => {
    if (!backdrop) return;
    const open = wrapper.classList.contains("toggled");
    backdrop.classList.toggle("show", open && isMobile());
  };

  btn.addEventListener("click", (e) => {
    e.preventDefault();
    wrapper.classList.toggle("toggled");
    syncBackdrop();
  });

  if (backdrop) backdrop.addEventListener("click", () => {
    wrapper.classList.remove("toggled");
    syncBackdrop();
  });

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      wrapper.classList.remove("toggled");
      syncBackdrop();
    }
  });

  window.addEventListener("resize", syncBackdrop);
});
