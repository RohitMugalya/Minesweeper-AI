# Minesweeper AI  

This project is an implementation of a Minesweeper game with an AI agent that uses logical reasoning to deduce safe cells and mines. The AI employs propositional logic to make decisions and interact with the game board.  

## Modules Overview  

- **`knowledge/`**: A Python package containing modules for logical reasoning:  
  - **`proposition.py`**: Defines the `Proposition` class and its subclasses (`Tautology` and `Contradiction`) to represent logical statements.  
  - **`connective.py`**: Implements logical connectives like `And`, `Or`, `Not`, `Imply`, and `BiConditional` for building logical expressions.  
- **`minesweeper.py`**: Contains the Minesweeper game logic and the AI agent (`MinesweeperAI`) that interacts with the game.  
- **`runner.py`**: Provides a graphical interface for playing the game using `pygame`.  
- **`test_knowledge.py`**: A test script to verify the logical reasoning capabilities of the AI.  

## Setup Instructions  

### 1. Clone the Repository  

Run the following command to clone the repository:  

```bash  
git clone https://github.com/RohitMugalya/Minesweeper-AI.git  
cd Minesweeper-AI  
```  

### 2. Create and Activate a Virtual Environment  

#### On Windows  

```bash  
python -m venv venv  
venv\Scripts\activate  
```  

#### On macOS/Linux  

```bash  
python3 -m venv venv  
source venv/bin/activate  
```  

### 3. Install Dependencies  

Run the following command to install the required dependencies:  

```bash  
pip install -r requirements.txt  
```  

### 4. Run the Game  

To start the Minesweeper game with the AI, execute:  

```bash  
python runner.py  
```  

Enjoy playing Minesweeper with an intelligent AI assistant!  

## Adjustable Variables and Parameters  

You can customize the game experience by modifying the following parameters in the `runner.py` file:  

- **`BOARD_HEIGHT`**: The number of rows in the Minesweeper grid.  
- **`BOARD_WIDTH`**: The number of columns in the Minesweeper grid.  
- **`CELL_SIZE`**: The size of each cell in pixels.  
- **`PROBABILITY_MINE`**: The probability of a cell containing a mine.  

For example, increasing `BOARD_HEIGHT` and `BOARD_WIDTH` will create a larger game board, while adjusting `PROBABILITY_MINE` changes the density of mines on the board.  

**Note**: Higher values for `BOARD_HEIGHT` and `BOARD_WIDTH` may result in slower performance due to the complexity of logical evaluations performed by the AI.  
