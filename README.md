# ChessArena 0G — AI Agent Battle Royale ♟

> Built for [Zero Cup 2026](https://0g.ai/arena/zero-cup) · Powered by **0G Chain** + **0G Storage**

## 🎯 What is ChessArena 0G?

ChessArena 0G is a **trustless AI chess tournament** where multiple AI agents battle each other in real-time. Every game is **verifiable**, every strategy is **immutable**, and every result is **on-chain**.

## 🔗 How 0G Makes This Possible (Not a Bolt-on!)

| Feature | Without 0G | With 0G |
|---------|-----------|---------|
| **Agent Strategies** | Stored on server → can be changed secretly | Hashed & locked on **0G Storage** → immutable, verifiable |
| **Game State** | Could be tampered with | All moves stored on **0G Storage** → tamper-proof |
| **Tournament Results** | "Trust us" | Posted to **0G Chain** → trustless, auditable |
| **Anti-Cheat** | Server-side only | **Strategy Lock** before game → cannot change mid-game |

### The 0G Integration Flow:
```
1. Player registers AI agent
   → Strategy code is hashed & stored on 0G Storage (Strategy Lock)
   → Hash is posted to 0G Chain as proof

2. Game begins
   → Each move's state is stored on 0G Storage
   → Game engine runs (verifiable execution)

3. Game ends
   → Result is posted to 0G Chain
   → Anyone can verify: strategy hash matches, no tampering

4. Leaderboard updates
   → Rankings computed from on-chain results
   → Trustless, transparent, auditable
```

## 🤖 AI Agents

| Agent | Strategy | Description |
|-------|----------|-------------|
| 🧠 Stockfish Lite | Minimax | Material-focused evaluator with 2-ply search |
| 🎯 Positional Pete | Positional | Center control & piece activity specialist |
| ⚔️ Aggressive Alex | Aggressive | Attack-focused, sacrifices for initiative |
| 🛡️ Defensive Diana | Defensive | Solid pawn structures, fortress builder |
| 🎲 Random Ron | Random | Plays random legal moves — chaos agent |
| 📚 Opening Oscar | Opening Book | Opening book specialist, middlegame weakness |

## 🚀 Quick Start

### Option 1: Open directly
```bash
open index.html
```

### Option 2: Serve with Python
```bash
python3 -m http.server 8080
# Open http://localhost:8080
```

### Option 3: Serve with Node.js
```bash
npx serve .
```

## 🎮 How to Play

1. **Select Agents**: Click on agent cards to assign them to White/Black
2. **Start Battle**: Click "▶ Start Battle" to begin
3. **Watch**: Watch the AI agents think and play in real-time
4. **Tournament**: Click "🏆 Tournament Mode" for round-robin matches
5. **Leaderboard**: ELO ratings update automatically after each game

## 📁 Project Structure

```
chessarena-0g/
├── index.html          # Main application (single-file)
├── README.md           # This file
├── contracts/
│   └── ChessArena.sol  # 0G Chain smart contract
└── docs/
    └── architecture.md # Architecture documentation
```

## 🔧 Smart Contract (0G Chain)

The `ChessArena.sol` contract handles:
- Agent registration with strategy hash
- Game state recording
- Result posting
- Leaderboard computation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│              Frontend (Browser)              │
│  ┌─────────┐  ┌──────────┐  ┌────────────┐ │
│  │ Chess   │  │ AI       │  │ 0G         │ │
│  │ Board   │  │ Agents   │  │ Integration│ │
│  │ (UI)    │  │ (Engine) │  │ (SDK)      │ │
│  └─────────┘  └──────────┘  └────────────┘ │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ 0G      │ │ 0G      │ │ 0G      │
   │ Chain   │ │ Storage │ │ Compute │
   │ (EVM)   │ │ (IPFS+) │ │ (AI)    │
   └─────────┘ └─────────┘ └─────────┘
```

## 📝 License

MIT — Built with ❤️ for the 0G ecosystem.

## 🏆 Zero Cup 2026

This project is built for the [Zero Cup 2026](https://0g.ai/arena/zero-cup) tournament by 0G.
