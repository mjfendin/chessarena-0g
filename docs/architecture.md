# ChessArena 0G — Architecture

## Overview

ChessArena 0G is a trustless AI chess tournament platform built on 0G infrastructure. The key innovation is that **0G does real work** — it's not a bolt-on:

- **0G Storage**: Stores immutable agent strategy hashes and game state
- **0G Chain**: Records tournament results, ELO ratings, and leaderboard on-chain
- **0G Compute**: (Future) Verifiable AI inference for agent moves

## System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Frontend (Browser)                     │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Chess   │  │   AI     │  │   0G     │  │  Game   │ │
│  │  Board   │  │  Agents  │  │   SDK    │  │  State  │ │
│  │ (UI/UX)  │  │ (Engine) │  │(Ethers.js│  │ Manager │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘ │
│       │              │              │              │      │
└───────┼──────────────┼──────────────┼──────────────┼──────┘
        │              │              │              │
        ▼              ▼              ▼              ▼
┌──────────────────────────────────────────────────────────┐
│                    Backend Services                       │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Game Engine │  │  Tournament  │  │  Strategy    │  │
│  │  (chess.js)  │  │  Manager     │  │  Locker      │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
└─────────┼──────────────────┼──────────────────┼──────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────┐
│                      0G Infrastructure                    │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   0G Chain   │  │  0G Storage  │  │  0G Compute  │  │
│  │  (EVM L1)    │  │  (Decentral) │  │  (AI Infra)  │  │
│  │              │  │              │  │              │  │
│  │ • Game       │  │ • Strategy   │  │ • AI Inference│ │
│  │   Results    │  │   Hashes     │  │   (Future)   │  │
│  │ • ELO        │  │ • Game State │  │              │  │
│  │   Ratings    │  │ • Move History│ │              │  │
│  │ • Leaderboard│  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Agent Registration
```
Player → Frontend → 0G Storage (strategy hash)
                  → 0G Chain (agent registration tx)
```

### 2. Strategy Lock (Pre-Game)
```
Agent Strategy Code
    ↓
SHA-256 Hash
    ↓
0G Storage (immutable storage)
    ↓
0G Chain (hash verification tx)
    ↓
Game cannot start until both strategies locked
```

### 3. Game Play
```
Each Move:
    1. AI Agent computes best move
    2. Move validated by chess.js
    3. Board state updated
    4. State hash stored on 0G Storage
    5. Move count recorded on 0G Chain
```

### 4. Game End
```
Game Result
    ↓
0G Storage (full game state hash)
    ↓
0G Chain (result tx + ELO update)
    ↓
Leaderboard recomputed from on-chain data
```

## Why 0G is Essential (Not Bolt-on)

### Problem: Trust in AI Tournaments
In a centralized chess arena:
- Server operator can change agent strategies mid-game
- Results can be faked
- Game history can be altered
- No way to prove fairness

### Solution: 0G Makes It Trustless
1. **Strategy Lock**: Before game starts, strategy hash is stored on 0G Storage. This hash is IMMUTABLE — the agent cannot change its strategy mid-game without changing the hash.

2. **Verifiable Results**: Every game result is posted to 0G Chain. Anyone can verify:
   - Strategy hash matches what was locked
   - Game state is consistent with moves
   - ELO calculations are correct

3. **Permanent History**: All game data is stored on 0G Storage permanently. Even if the frontend goes down, the data persists.

## Smart Contract (ChessArena.sol)

The on-chain contract handles:
- `registerAgent()`: Register AI agent with strategy hash
- `lockStrategy()`: Lock strategy hash (immutable)
- `startGame()`: Begin a game between two agents
- `recordMove()`: Record each move on-chain
- `finishGame()`: Post result and update ELO
- `getAgentStats()`: Query agent's current stats

## Frontend Components

### Chess Board (chessboard.js)
- Visual representation of the game
- Real-time updates as moves are made
- Piece animation for smooth gameplay

### AI Agents (chess.js + custom strategies)
- Multiple AI agents with different play styles
- Material evaluation, positional play, aggressive, defensive
- Opening book for realistic play

### 0G Integration Panel
- Shows connection status to 0G Chain and Storage
- Displays strategy hashes
- Logs all on-chain transactions

### Leaderboard
- Real-time ELO updates
- Win/loss/draw statistics
- Rankings sorted by ELO

## Future Enhancements

1. **0G Compute Integration**: Run AI inference on 0G Compute Network for verifiable agent decisions
2. **Multi-Table Tournaments**: Swiss-system or round-robin tournaments
3. **Spectator Mode**: Real-time viewing of ongoing games
4. **Agent Marketplace**: Buy/sell verified agent strategies
5. **Prize Distribution**: On-chain prize distribution based on tournament results

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Chess Logic**: chess.js 0.10.3
- **Chess Board**: chessboard.js 1.0.0
- **0G Chain**: EVM-compatible (ethers.js)
- **0G Storage**: 0G Storage SDK
- **Smart Contracts**: Solidity 0.8.19
