// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title ChessArena 0G — Tournament Contract
 * @notice 2 TX per game: startMatch (register+lock+start) + recordGameResult
 * @dev Built for Zero Cup 2026 — 0G Arena
 */
contract ChessArena0G {

    struct Agent {
        string name;
        string strategyHash;
        uint256 elo;
        uint256 wins;
        uint256 losses;
        uint256 draws;
        bool active;
    }

    struct Game {
        string whiteName;
        string blackName;
        string whiteStrategy;
        string blackStrategy;
        string result;
        uint256 totalMoves;
        string movesData;
        string stateHash;
        uint256 startedAt;
        uint256 endedAt;
        bool completed;
    }

    uint256 public agentCount;
    uint256 public gameCount;
    mapping(uint256 => Agent) public agents;
    mapping(string => uint256) public agentNameToId;
    mapping(uint256 => Game) public games;

    event AgentRegistered(uint256 indexed agentId, string name, string strategyHash);
    event StrategyLocked(uint256 indexed agentId, string strategyHash);
    event MatchStarted(uint256 indexed gameId, string whiteName, string blackName);
    event GameRecorded(uint256 indexed gameId, string result, uint256 totalMoves, address recordedBy);

    function startMatch(
        string calldata _whiteName,
        string calldata _whiteStrategy,
        string calldata _blackName,
        string calldata _blackStrategy
    ) external returns (uint256) {
        uint256 whiteId = _registerOrGetAgent(_whiteName, _whiteStrategy, msg.sender);
        uint256 blackId = _registerOrGetAgent(_blackName, _blackStrategy, msg.sender);

        gameCount++;
        games[gameCount] = Game({
            whiteName: _whiteName,
            blackName: _blackName,
            whiteStrategy: _whiteStrategy,
            blackStrategy: _blackStrategy,
            result: "",
            totalMoves: 0,
            movesData: "",
            stateHash: "",
            startedAt: block.timestamp,
            endedAt: 0,
            completed: false
        });

        emit MatchStarted(gameCount, _whiteName, _blackName);
        return gameCount;
    }

    function recordGameResult(
        uint256 _gameId,
        string calldata _result,
        uint256 _totalMoves,
        string calldata _movesData,
        string calldata _stateHash
    ) external {
        Game storage g = games[_gameId];
        require(!g.completed, "Already completed");

        g.result = _result;
        g.totalMoves = _totalMoves;
        g.movesData = _movesData;
        g.stateHash = _stateHash;
        g.endedAt = block.timestamp;
        g.completed = true;

        _updateElo(g.whiteName, g.blackName, _result);
        emit GameRecorded(_gameId, _result, _totalMoves, msg.sender);
    }

    function getAgentStats(string calldata _name) external view returns (string memory, uint256, uint256, uint256, uint256) {
        uint256 id = agentNameToId[_name];
        Agent storage a = agents[id];
        return (a.name, a.elo, a.wins, a.losses, a.draws);
    }

    function getGame(uint256 _gameId) external view returns (string memory, string memory, string memory, uint256, bool) {
        Game storage g = games[_gameId];
        return (g.whiteName, g.blackName, g.result, g.totalMoves, g.completed);
    }

    function _registerOrGetAgent(string calldata _name, string calldata _strategy, address _owner) internal returns (uint256) {
        uint256 id = agentNameToId[_name];
        if (id == 0) {
            agentCount++;
            id = agentCount;
            agents[id] = Agent(_name, _strategy, 1200, 0, 0, 0, true);
            agentNameToId[_name] = id;
            emit AgentRegistered(id, _name, _strategy);
        } else {
            agents[id].strategyHash = _strategy;
        }
        emit StrategyLocked(id, _strategy);
        return id;
    }

    function _updateElo(string memory _whiteName, string memory _blackName, string memory _result) internal {
        uint256 whiteId = agentNameToId[_whiteName];
        uint256 blackId = agentNameToId[_blackName];

        if (whiteId == 0 || blackId == 0) return;

        uint256 wElo = agents[whiteId].elo;
        uint256 bElo = agents[blackId].elo;

        if (keccak256(abi.encodePacked(_result)) == keccak256(abi.encodePacked("white"))) {
            agents[whiteId].elo = wElo + 32;
            agents[blackId].elo = bElo > 32 ? bElo - 32 : 800;
            agents[whiteId].wins++;
            agents[blackId].losses++;
        } else if (keccak256(abi.encodePacked(_result)) == keccak256(abi.encodePacked("black"))) {
            agents[whiteId].elo = wElo > 32 ? wElo - 32 : 800;
            agents[blackId].elo = bElo + 32;
            agents[whiteId].losses++;
            agents[blackId].wins++;
        } else {
            agents[whiteId].draws++;
            agents[blackId].draws++;
        }
    }
}
