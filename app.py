from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

game_state = {
    "players": {
        "player1": {"y": 200},
        "player2": {"y": 200}
    },
    "ball": {"x": 300, "y": 200, "vx": 4, "vy": 4},
    "active": False  # Initially inactive until 2 players join
}

sid_to_player = {}
room_name = "game_room"

def check_and_update_game_active():
    # Enable game only if exactly 2 players connected
    if len(sid_to_player) == 2:
        game_state["active"] = True
    else:
        game_state["active"] = False

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on("join")
def handle_join(data):
    sid = request.sid
    username = data.get("username", "Unknown")
    join_room(room_name)

    if "player1" not in sid_to_player.values():
        sid_to_player[sid] = "player1"
        game_state["players"]["player1"]["username"] = username
    else:
        sid_to_player[sid] = "player2"
        game_state["players"]["player2"]["username"] = username

    check_and_update_game_active()

    emit("joined", {
        "player": sid_to_player[sid],
        "opponent": game_state["players"].get("player2" if sid_to_player[sid] == "player1" else "player1", {}).get("username", "")
    }, room=sid)

    print(f"{sid_to_player[sid]} joined, players count: {len(sid_to_player)}")


@socketio.on("leave")
def handle_leave():
    sid = request.sid
    player = sid_to_player.pop(sid, None)
    leave_room(room_name)
    check_and_update_game_active()
    socketio.emit("opponent_left", {"player": player}, room=room_name)
    print(f"{player} left the game")

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    player = sid_to_player.pop(sid, None)
    leave_room(room_name)
    check_and_update_game_active()
    socketio.emit("opponent_left", {"player": player}, room=room_name)
    print(f"{player} disconnected")

@socketio.on("move_paddle")
def handle_paddle_move(data):
    sid = request.sid
    player_id = sid_to_player.get(sid)
    if not player_id or not game_state["active"]:
        return
    if data["direction"] == "up":
        game_state["players"][player_id]["y"] = max(0, game_state["players"][player_id]["y"] - 5)
    elif data["direction"] == "down":
        game_state["players"][player_id]["y"] = min(300, game_state["players"][player_id]["y"] + 5)


def game_loop():
    while True:
        if not game_state["active"]:
            time.sleep(1 / 60)
            continue

        ball = game_state["ball"]
        ball["x"] += ball["vx"]
        ball["y"] += ball["vy"]

        # Wall collision
        if ball["y"] <= 0 or ball["y"] >= 400:
            ball["vy"] *= -1

        # Paddle collision
        p1_y = game_state["players"]["player1"]["y"]
        p2_y = game_state["players"]["player2"]["y"]

        if ball["x"] <= 20 and p1_y < ball["y"] < p1_y + 100:
            ball["vx"] *= -1
        elif ball["x"] >= 580 and p2_y < ball["y"] < p2_y + 100:
            ball["vx"] *= -1

        # Reset if ball goes off screen
        if ball["x"] <= 0 or ball["x"] >= 600:
            ball["x"], ball["y"] = 300, 200

        socketio.emit("game_state", game_state, room=room_name)
        time.sleep(1 / 60)

threading.Thread(target=game_loop, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
