const randomChoice = (choices) => choices[Math.floor(Math.random() * choices.length)];

document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.querySelector('#viewport');
    const button = document.querySelector('#activate');

    const nInput = document.querySelector('#n-input');
    const dInput = document.querySelector('#d-input');
    const phiInput = document.querySelector('#phi-input');
    
    const context = canvas.getContext('2d');
    const { width, height } = canvas;

    button.onclick = () => {
        fetch(`/galaxy/create?n=${nInput.value}&d=${dInput.value}&phi=${phiInput.value}`, { credentials: "include" })
            .then(response => response.json())
            .then(systems => {
                context.clearRect(0, 0, width, height);
                systems.forEach(system => {
                    let [ x, y ] = system.coordinates;
                    x += width / 2;
                    y += height / 2;
                    context.fillStyle = randomChoice(['red', 'green', 'blue']);
                    context.fillRect(x, y, 1, 1);
                });
            })
            .catch(error => alert(error));
    };
});