const direction = document.getElementById("joystick-container");
const joystick = document.getElementById("joystick");
const output = document.getElementById("output");
const buttonShoot = document.getElementById("shoot");
const buttonRotateCW = document.getElementById("rotate-cw");
const buttonRotateCCW = document.getElementById("rotate-ccw");

const urlParams = new URLSearchParams(window.location.search);
const lang = urlParams.get('lang');
const player_id = urlParams.get('player_id');

const center = 100;
const maxDistance = 80;

var movementDirection = "stop";
var rotationDirection = "stop";

const events = {
    move: {
        up: 5,
        up_right: 6,
        right: 7,
        down_right: 8,
        down: 9,
        down_left: 10,
        left: 11,
        up_left: 12,
        stop: 13
    },
    rotate: {
        cw: 16,
        ccw: 17,
        stop: 18
    },
    shoot: 19,
    join: 20
}

function sendToBackend(data) {
    const apiUrl = `${window.location.protocol}//${window.location.hostname}:${window.location.port}/api/events`;
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

function generateJoystickFeedback() {
    navigator.vibrate(10);
}

function getPosition(e) {
    const rect = direction.getBoundingClientRect();
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

    const joyXInt = Math.round(joyX / maxDistance);
    const joyYInt = Math.round(joyY / maxDistance);
    
    var localMovementDirection = "";

    if (joyYInt > 0) {
        localMovementDirection = "down";
    }
    else if (joyYInt < 0) {
        localMovementDirection = "up"; 
    }

    if (joyXInt > 0) {
        localMovementDirection += localMovementDirection ? "_right" : "right";
    }
    else if (joyXInt < 0) {
        localMovementDirection += localMovementDirection ? "_left" : "left";
    }

    if (localMovementDirection && localMovementDirection != movementDirection)
    {
        movementDirection = localMovementDirection;
        sendToBackend({
            player_id: player_id,
            event: events.move[localMovementDirection],
            lang: lang
        });
    }
}

function resetJoystick() {
    joystick.style.left = "70px";
    joystick.style.top = "70px";
    movementDirection = "stop";
    
}

direction.addEventListener("mousedown", (e) => {
    document.onmousemove = (e) => moveJoystick(...Object.values(getPosition(e)));
    document.onmouseup = () => {
        document.onmousemove = null;
        resetJoystick();
    };
});

direction.addEventListener("touchstart", () => {
    resetJoystick();
    generateJoystickFeedback();
});

buttonShoot.addEventListener("touchstart", () => {
    sendToBackend({
        player_id: player_id,
        event: events.shoot
    });
    generateJoystickFeedback();
});

buttonRotateCW.addEventListener("touchstart", () => {
    sendToBackend({
        player_id: player_id,
        event: events.rotate.cw
    });
    generateJoystickFeedback();
});

buttonRotateCCW.addEventListener("touchstart", () => {
    sendToBackend({
        player_id: player_id,
        event: events.rotate.ccw
    });
    generateJoystickFeedback();
});

buttonRotateCW.addEventListener("touchend", () => {
    sendToBackend({
        player_id: player_id,
        event: events.rotate.stop
    });
    generateJoystickFeedback();
});

buttonRotateCCW.addEventListener("touchend", () => {
    sendToBackend({
        player_id: player_id,
        event: events.rotate.stop
    });
    generateJoystickFeedback();
});

direction.addEventListener("touchend", (e) => {
    sendToBackend({
        player_id: player_id,
        event: events.move.stop
    });
    resetJoystick();
    generateJoystickFeedback();
});

direction.addEventListener("touchmove", (e) => {
    moveJoystick(...Object.values(getPosition(e)));
});

window.addEventListener('load', function() {
    sendToBackend({
        player_id: player_id,
        event: events.join,
        lang: lang
    });
});