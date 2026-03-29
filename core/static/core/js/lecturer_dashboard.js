console.log("Lecturer dashboard loaded");

document.addEventListener('DOMContentLoaded', () => {
    const navList = document.querySelector('.nav-links');
    const sections = document.querySelectorAll('.content-section');

    if (navList) {
        navList.addEventListener('click', (e) => {
            const link = e.target.closest('.nav-link');
            if (!link) return;
            e.preventDefault();

            const target = link.dataset.section;
            if (!target) return;

            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            sections.forEach(section => section.classList.remove('active'));
            const activeSection = document.getElementById(target);
            if (activeSection) {
                activeSection.classList.add('active');
            }
        });
    }
});
