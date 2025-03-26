const closeGameButton = document.getElementById("close-game-window");
const gameAppIcon = document.getElementById("open-game-app");
let appOpen = true;

async function openGameApp() {
    if (appOpen === false) {
        console.log("Opened!");
        appOpen = true;
    }
}
async function closeGameApp() {
    if (appOpen) {
        console.log("Closed!");
        appOpen = false;
    }
}
if (appOpen) {
    closeGameButton.addEventListener("click", closeGameApp);
} else {
    gameAppIcon.addEventListener("click", openGameApp);
}
