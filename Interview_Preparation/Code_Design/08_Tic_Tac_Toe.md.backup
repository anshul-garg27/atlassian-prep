# ⭕❌ PROBLEM 8: TIC TAC TOE GAME

### ⭐⭐⭐ **Design Tic Tac Toe with Strategy Pattern**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Easy-Medium
**Focus:** Game Logic, Win Detection, Extensibility

---

## 📋 Problem Statement

Design Tic Tac Toe game with:
- N×N board (3×3 default)
- 2 players (X and O)
- Win detection (row, column, diagonal)
- Support for AI players (extension)

---

## 💻 Implementation

```java
enum Player {
    X, O, NONE
}

class Board {
    private Player[][] grid;
    private int size;
    
    public Board(int size) {
        this.size = size;
        this.grid = new Player[size][size];
        for (int i = 0; i < size; i++) {
            Arrays.fill(grid[i], Player.NONE);
        }
    }
    
    public boolean makeMove(int row, int col, Player player) {
        if (row < 0 || row >= size || col < 0 || col >= size) {
            return false;
        }
        if (grid[row][col] != Player.NONE) {
            return false;
        }
        grid[row][col] = player;
        return true;
    }
    
    public Player checkWinner() {
        // Check rows
        for (int i = 0; i < size; i++) {
            if (grid[i][0] != Player.NONE &&
                allEqual(grid[i])) {
                return grid[i][0];
            }
        }
        
        // Check columns
        for (int j = 0; j < size; j++) {
            Player first = grid[0][j];
            if (first != Player.NONE) {
                boolean win = true;
                for (int i = 1; i < size; i++) {
                    if (grid[i][j] != first) {
                        win = false;
                        break;
                    }
                }
                if (win) return first;
            }
        }
        
        // Check main diagonal
        if (grid[0][0] != Player.NONE) {
            boolean win = true;
            for (int i = 1; i < size; i++) {
                if (grid[i][i] != grid[0][0]) {
                    win = false;
                    break;
                }
            }
            if (win) return grid[0][0];
        }
        
        // Check anti-diagonal
        if (grid[0][size-1] != Player.NONE) {
            boolean win = true;
            for (int i = 1; i < size; i++) {
                if (grid[i][size-1-i] != grid[0][size-1]) {
                    win = false;
                    break;
                }
            }
            if (win) return grid[0][size-1];
        }
        
        return Player.NONE;
    }
    
    private boolean allEqual(Player[] row) {
        for (int i = 1; i < row.length; i++) {
            if (row[i] != row[0]) return false;
        }
        return true;
    }
    
    public boolean isFull() {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (grid[i][j] == Player.NONE) return false;
            }
        }
        return true;
    }
    
    public void print() {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                System.out.print(grid[i][j] == Player.NONE ? "." : grid[i][j]);
                System.out.print(" ");
            }
            System.out.println();
        }
    }
}

class TicTacToeGame {
    private Board board;
    private Player currentPlayer;
    private Player winner;
    
    public TicTacToeGame(int boardSize) {
        this.board = new Board(boardSize);
        this.currentPlayer = Player.X;
        this.winner = Player.NONE;
    }
    
    public boolean makeMove(int row, int col) {
        if (winner != Player.NONE) {
            System.out.println("Game over!");
            return false;
        }
        
        if (board.makeMove(row, col, currentPlayer)) {
            winner = board.checkWinner();
            if (winner != Player.NONE) {
                System.out.println("Winner: " + winner);
            } else if (board.isFull()) {
                System.out.println("Draw!");
            } else {
                switchPlayer();
            }
            return true;
        }
        return false;
    }
    
    private void switchPlayer() {
        currentPlayer = (currentPlayer == Player.X) ? Player.O : Player.X;
    }
    
    public void printBoard() {
        board.print();
    }
}
```

---

## 🚀 Extensions

### **1. AI Player (Minimax)**
```java
class AIPlayer {
    public int[] getBestMove(Board board, Player player) {
        int[] bestMove = new int[2];
        int bestScore = Integer.MIN_VALUE;
        
        for (int i = 0; i < board.size; i++) {
            for (int j = 0; j < board.size; j++) {
                if (board.canPlace(i, j)) {
                    board.makeMove(i, j, player);
                    int score = minimax(board, 0, false, player);
                    board.undo(i, j);
                    
                    if (score > bestScore) {
                        bestScore = score;
                        bestMove[0] = i;
                        bestMove[1] = j;
                    }
                }
            }
        }
        return bestMove;
    }
    
    private int minimax(Board board, int depth, boolean isMaximizing, Player player) {
        // Implementation of minimax algorithm
        // ...
    }
}
```

### **2. Undo Feature**
```java
class Move {
    int row, col;
    Player player;
}

class Game {
    Stack<Move> moveHistory = new Stack<>();
    
    public void undo() {
        if (!moveHistory.isEmpty()) {
            Move lastMove = moveHistory.pop();
            board.clear(lastMove.row, lastMove.col);
            switchPlayer();
        }
    }
}
```

---

## 💡 Interview Tips

✅ **O(1) win check** using counters (optional optimization)
✅ **Strategy Pattern** for AI players
✅ Support **N×N** boards (not just 3×3)
✅ **Undo/Redo** functionality
✅ **Multiplayer** over network

**Easy problem, but ask about extensions!**
