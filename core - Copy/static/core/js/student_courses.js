function toggleCourse(element) {
    const materials = element.nextElementSibling;

    if (materials.style.display === "block") {
        materials.style.display = "none";
    } else {
        materials.style.display = "block";
    }
}