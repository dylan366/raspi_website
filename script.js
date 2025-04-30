// opening and closing game window with icon
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


// handling the queue and play button
const joinQueueButton = document.getElementById("joinGameQueue");
const leaveQueueButton = document.getElementById("leaveGameQueue");
let inQueue = false;
leaveQueueButton.style.visibility = "hidden";
const usernameInput = document.getElementById("username-input");

async function clickJoinQueue() {
    if (inQueue == false && appOpen == true && usernameInput.value != "" && !usernameInput.value.includes(" ")) {
        console.log("Joined queue with username: ");
        console.log(usernameInput.value);
        inQueue = true;
        joinQueueButton.style.visibility = "hidden";
        leaveQueueButton.style.visibility = "visible";
    }
}

async function clickLeaveQueue() {
    if (inQueue == true) {
        console.log("Left queue!");
        inQueue = false;
        joinQueueButton.style.visibility = "visible";
        leaveQueueButton.style.visibility = "hidden";
    }
}

joinQueueButton.addEventListener("click", clickJoinQueue);
leaveQueueButton.addEventListener("click", clickLeaveQueue);
