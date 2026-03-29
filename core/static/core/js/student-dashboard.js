// JS placeholder for future features
// Example: dynamic card updates, notifications, etc.
console.log("Student Dashboard JS loaded");

document.addEventListener('DOMContentLoaded', () => {
    // Sidebar navigation logic (event delegation for reliability)
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

    // Expand materials on click
    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach(card => {
        card.addEventListener('click', () => {
            const materials = card.querySelector('.materials');
            if (!materials) return;
            card.classList.toggle('active');
        });

        const innerActions = card.querySelectorAll('a, button');
        innerActions.forEach(action => {
            action.addEventListener('click', (e) => {
                e.stopPropagation();
            });
        });
    });
});
