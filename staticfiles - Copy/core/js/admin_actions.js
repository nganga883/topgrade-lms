document.querySelectorAll("form").forEach(form=>{
    form.addEventListener("submit", e=>{
        if(!confirm("Are you sure?")){
            e.preventDefault();
        }
    });
});