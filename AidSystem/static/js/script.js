
  // إخفاء الـ Loader بعد تحميل الصفحة
window.addEventListener("load", () => {
    const loader = document.getElementById("loader");
    setTimeout(() => {
    loader.style.opacity = "0";
    loader.style.visibility = "hidden";
}, 600);

    // إظهار عناصر fade-in بعد التحميل
    document.querySelectorAll('.fade-in').forEach(el => {
    setTimeout(() => el.classList.add('show'), 100);
    });
});

  // زر الرجوع لأعلى
const scrollBtn = document.getElementById("scrollTopBtn");

window.onscroll = function () {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
    scrollBtn.style.display = "block";
    } else {
    scrollBtn.style.display = "none";
    }
};

scrollBtn.onclick = function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

