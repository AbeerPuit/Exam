function addQuestion() {
    const container = document.getElementById("questionsContainer");
    const block = container.children[0].cloneNode(true);
    
    // Clear the cloned input fields
    block.querySelectorAll("input, textarea, select").forEach(input => {
        input.value = "";
    });

    container.appendChild(block);
}
