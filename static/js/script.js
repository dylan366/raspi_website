const canvas = document.getElementById("canvas-game");
const ctx = canvas.getContext("2d");
const socket = io();

let player = "";
let inGame = false;

const paddleWidth = 10;
const paddleHeight = 100;
let gameState = {
    players: {
        player1: { y: 200 },
        player2: { y: 200 }
    },
    ball: { x: 300, y: 200 }
};

// app open close on website
const closeGameButton = document.getElementById("close-game-window");
const gameAppIcon = document.getElementById("open-game-app");
const gameWindow = document.getElementById("game-application-window");
let appOpen = false;

gameWindow.style.display = "none";

gameAppIcon.addEventListener("dblclick", () => {
    gameWindow.style.display = "grid";
    appOpen = true;
    console.log("App opened");
});
closeGameButton.addEventListener("click", () => {
    gameWindow.style.display = "none";
    appOpen = false;
    console.log("App closed");
});

// queue buttons and stuff
const joinQueueButton = document.getElementById("joinGameQueue");
const leaveQueueButton = document.getElementById("leaveGameQueue");
const usernameInput = document.getElementById("username-input");
const opponentUsernameLabel = document.getElementById("other-ip-address");

joinQueueButton.style.visibility = "visible";
leaveQueueButton.style.visibility = "hidden";

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // draw ball
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(gameState.ball.x, gameState.ball.y, 10, 0, Math.PI * 2);
    ctx.fill();

    // draw paddles
    ctx.fillRect(10, gameState.players.player1.y, paddleWidth, paddleHeight);
    ctx.fillRect(580, gameState.players.player2.y, paddleWidth, paddleHeight);
}

function joinGame() {
    if (appOpen) {
        const username = document.getElementById("username-input").value.trim();
        if (username === "") {
            alert("Enter a valid username");
            return;
        }
        if (username.includes(" ")) {
            alert("Enter a valid username")
            return;
        }
        socket.emit("join", { username });

        joinQueueButton.style.visibility = "hidden";
        leaveQueueButton.style.visibility = "visible";
        usernameInput.readOnly = true;
        console.log("joined queue");
    }
}

function leaveGame() {
    if (inGame) {
            socket.emit("leave");
            inGame = false;
            alert("You have left the game.");
            clearCanvas();
            joinQueueButton.style.visibility = "visible";
            leaveQueueButton.style.visibility = "hidden";
            usernameInput.readOnly = false;
    }
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// bunch of sockets (send stuff to python and back)
socket.on("joined", (data) => {
    player = data.player;
    inGame = true;
    console.log("You are:", player);
});

socket.on("game_state", (state) => {
    if (!inGame || !state.active) {
        return;
    }
    gameState = state;
    draw();
});

socket.on("opponent_left", () => {
    inGame = false;
    alert("Your opponent has left the game.");
    clearCanvas();
});

document.addEventListener("keydown", (e) => {
    if (!inGame) {
        return;
    }
    if (e.key === "ArrowUp") {
        socket.emit("move_paddle", { direction: "up" });
    } else if (e.key === "ArrowDown") {
        socket.emit("move_paddle", { direction: "down" });
    }
});

joinQueueButton.addEventListener("click", joinGame);
leaveQueueButton.addEventListener("click", leaveGame);

