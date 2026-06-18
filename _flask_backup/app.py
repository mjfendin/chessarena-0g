"""
ChessArena 0G — Main Application
Flask + SocketIO web server for the AI Chess Battle Royale.
"""
import asyncio
import logging
import os
import sys
import json
import hashlib
import time

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chess_engine import ChessGame, RandomAgent, MinimaxAgent, AgentRegistry
from src.storage import ZeroGStorage
from src.chain import ZeroGChain
from src.tournament import Tournament

# ── Logging ─────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger("chessarena")

# ── Flask App ───────────────────────────────────────────────────────
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET", "chessarena-0g-secret")
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

# ── 0G Services ─────────────────────────────────────────────────────
storage = ZeroGStorage(mock=True)  # Set mock=False when 0G is configured
chain = ZeroGChain(mock=True)      # Set mock=False when contract is deployed

# ── Tournament State ────────────────────────────────────────────────
tournament: Tournament = None
game_state = {
    "board_fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "moves": [],
    "white": "White",
    "black": "Black",
    "status": "waiting",
    "result": None,
}

# ── Routes ──────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def api_status():
    return jsonify({
        "status": "online",
        "tournament": tournament.get_status() if tournament else None,
        "leaderboard": chain.get_leaderboard(),
    })

@app.route("/api/leaderboard")
def api_leaderboard():
    return jsonify(chain.get_leaderboard())

@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.json
    agent_id = data.get("agent_id", "").strip()
    agent_type = data.get("agent_type", "random")
    strategy_code = data.get("strategy_code", "")

    if not agent_id:
        return jsonify({"error": "agent_id is required"}), 400

    if tournament is None:
        init_tournament()

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(
        tournament.register_agent(agent_id, agent_type, strategy_code,
                                   hashlib.sha256(strategy_code.encode()).hexdigest())
    )
    loop.close()

    return jsonify(result)

@app.route("/api/start", methods=["POST"])
def api_start():
    global tournament
    if tournament is None:
        return jsonify({"error": "No tournament initialized. Register agents first."}), 400

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(tournament.start_tournament())
    loop.close()

    return jsonify(result)

@app.route("/api/play", methods=["POST"])
def api_play():
    if tournament is None or tournament.status != "active":
        return jsonify({"error": "No active tournament"}), 400

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(tournament.run_next_match())
    loop.close()

    if result:
        # Update game state with latest result
        game_state["status"] = "completed"
        game_state["result"] = result["result"]
        socketio.emit("match_result", result)

    return jsonify(result or {"message": "Tournament completed"})

@app.route("/api/play_all", methods=["POST"])
def api_play_all():
    """Play all remaining matches in the tournament."""
    if tournament is None or tournament.status != "active":
        return jsonify({"error": "No active tournament"}), 400

    results = []
    loop = asyncio.new_event_loop()
    while True:
        pending = tournament.bracket.get_pending_matches() if tournament.bracket else []
        if not pending:
            break
        result = loop.run_until_complete(tournament.run_next_match())
        if result:
            results.append(result)
    loop.close()

    return jsonify({"matches": results, "status": tournament.status})

@app.route("/api/game/<game_id>")
def api_game(game_id):
    for match in (tournament.matches if tournament else []):
        if match.match_id == game_id:
            return jsonify(match.to_dict())
    return jsonify({"error": "Game not found"}), 404


# ── WebSocket Events ────────────────────────────────────────────────

@socketio.on("connect")
def handle_connect():
    logger.info("Client connected")
    emit("game_state", game_state)

@socketio.on("disconnect")
def handle_disconnect():
    logger.info("Client disconnected")


# ── Tournament Callback ─────────────────────────────────────────────

async def tournament_callback(event_type: str, data: dict):
    """Callback for tournament events -> broadcast to all clients."""
    socketio.emit(event_type, data)


def init_tournament():
    global tournament
    tournament = Tournament(storage, chain, callback=tournament_callback)
    logger.info(f"Tournament initialized: {tournament.tournament_id}")


# ── Main ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8501"))
    logger.info(f"ChessArena 0G starting on port {port}")
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
