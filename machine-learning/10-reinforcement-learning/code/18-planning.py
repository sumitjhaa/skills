"""10.18 Planning: MCTS on a simple Tic-Tac-Toe game."""
import numpy as np

SIZE = 3
N_SIMS = 200
C = 1.4


def check_win(board):
    for i in range(3):
        if abs(board[i].sum()) == 3 or abs(board[:, i].sum()) == 3:
            return True
    if abs(board.trace()) == 3 or abs(np.fliplr(board).trace()) == 3:
        return True
    return False


def available(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r, c] == 0]


class Node:
    def __init__(self, board, player, parent=None, action=None):
        self.board = board.copy()
        self.player = player
        self.parent = parent
        self.action = action
        self.children = {}
        self.N = 0
        self.W = 0
        self.untried = available(board)

    def ucb(self, c):
        if self.N == 0:
            return float('inf')
        return self.W / self.N + c * np.sqrt(np.log(self.parent.N) / self.N) if self.parent else self.W / self.N


def mcts(root, n_sims):
    for _ in range(n_sims):
        node = root
        # Selection
        while node.untried == [] and node.children:
            node = max(node.children.values(), key=lambda n: n.ucb(C))
        # Expansion
        if node.untried:
            action = node.untried.pop()
            new_board = node.board.copy()
            new_board[action] = node.player
            child = Node(new_board, -node.player, node, action)
            node.children[action] = child
            node = child
        # Rollout
        b = node.board.copy()
        p = node.player
        moves = available(b)
        while moves and not check_win(b):
            a = moves[np.random.randint(len(moves))]
            b[a] = p
            p = -p
            moves = available(b)
        result = 1 if check_win(b) and node.player == 1 else -1 if check_win(b) else 0
        # Backup
        while node:
            node.N += 1
            node.W += result
            node = node.parent

    return max(root.children.values(), key=lambda n: n.N).action


board = np.zeros((3, 3), dtype=int)
print("Initial board:\n", board)
action = mcts(Node(board, 1), N_SIMS)
board[action] = 1
print(f"MCTS plays at {action}:")
print(board)
print("MCTS planning complete.")
