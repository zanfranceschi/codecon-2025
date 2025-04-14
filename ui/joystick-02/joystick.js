const container = document.getElementById("joystick-container");
const joystick = document.getElementById("joystick");
const output = document.getElementById("output");
const buttonOutput = document.getElementById("button-output");

const center = 100;
const maxDistance = 80;

function sendToBackend(data) {
    const apiUrl = `http://${window.location.hostname}:8000/events`;
    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).catch(err => {
        console.error("Erro ao enviar dados:", err);
    });
}

function getPosition(e) {
    const rect = container.getBoundingClientRect();
    const x = (e.touches ? e.touches[0].clientX : e.clientX) - rect.left;
    const y = (e.touches ? e.touches[0].clientY : e.clientY) - rect.top;
    return { x, y };
}

function moveJoystick(x, y) {
    const dx = x - center;
    const dy = y - center;
    const distance = Math.min(Math.sqrt(dx * dx + dy * dy), maxDistance);
    const angle = Math.atan2(dy, dx);

    const joyX = Math.cos(angle) * distance;
    const joyY = Math.sin(angle) * distance;

    joystick.style.left = `${center + joyX - 30}px`;
    joystick.style.top = `${center + joyY - 30}px`;

    output.textContent = `X: ${(joyX / maxDistance).toFixed(2)} | Y: ${(joyY / maxDistance).toFixed(2)}`;

    sendToBackend({
        player_id: "zan",
        event: 1,
        lang: "clojure"
    });
}

function resetJoystick() {
    joystick.style.left = "70px";
    joystick.style.top = "70px";
    output.textContent = "X: 0 | Y: 0";
}

container.addEventListener("mousedown", (e) => {
    document.onmousemove = (e) => moveJoystick(...Object.values(getPosition(e)));
    document.onmouseup = () => {
        document.onmousemove = null;
        resetJoystick();
    };
});

container.addEventListener("touchstart", (e) => {
    document.ontouchmove = (e) => moveJoystick(...Object.values(getPosition(e)));
    document.ontouchend = () => {
        document.ontouchmove = null;
        resetJoystick();
    };
});

// Botões
document.querySelectorAll(".joy-button").forEach((btn) => {
    btn.addEventListener("click", () => {
        const label = btn.getAttribute("data-btn");
        buttonOutput.textContent = `Botão: ${label}`;
        console.log(`Botão ${label} pressionado`);
    });
});
