const closeGameButton = document.getElementById("close-game-window");
const gameAppIcon = document.getElementById("open-game-app");
const gameWindow = document.getElementById("game-application-window");

let appOpen = false;

async function openGameApp() {
    if (appOpen === false) {
        console.log("Opened!");
        gameWindow.style.display = "grid";
        appOpen = true;
    }
}
async function closeGameApp() {   
    if (appOpen === true) {
        console.log("Closed!");
        gameWindow.style.display = "none";
        appOpen = false;
    }
}

closeGameButton.addEventListener("click", closeGameApp);
gameAppIcon.addEventListener("dblclick", openGameApp);

gameWindow.style.display = "none";