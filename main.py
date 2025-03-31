print("before import")
from random import choice
import csv
print("after import")


class TreeNode:
    """Represents a node in the binary search tree for storing words."""
    def __init__(self, word):
        self.word = word
        self.left = None
        self.right = None

class WordTree:
    """Binary Search Tree (BST) to store words for the game."""
    def __init__(self):
        self.root = None

    def insert(self, word):
        """Insert a word into the BST."""
        if self.root is None:
            self.root = TreeNode(word)
        else:
            self._insert_recursive(self.root, word)

    def _insert_recursive(self, node, word):
        if word < node.word:
            if node.left is None:
                node.left = TreeNode(word)
            else:
                self._insert_recursive(node.left, word)
        elif word > node.word:
            if node.right is None:
                node.right = TreeNode(word)
            else:
                self._insert_recursive(node.right, word)

    def get_random_word(self):
        """Retrieve a random word from the BST."""
        words = []
        self._in_order_traversal(self.root, words)
        return choice(words) if words else None

    def _in_order_traversal(self, node, words):
        """Perform an in-order traversal to collect words."""
        if node:
            self._in_order_traversal(node.left, words)
            words.append(node.word)
            self._in_order_traversal(node.right, words)


class GameState:
    """Manages game state using a CSV file."""
    def __init__(self, file_path="game_state.csv"):
        self.file_path = file_path
        self.game_data = {}

    def load_game_data(self):
        """Load game states from CSV into a dictionary."""
        try:
            with open(self.file_path, newline="", mode="r") as file:
                reader = csv.DictReader(file)
                self.game_data = {row["Name"]: row for row in reader}
        except FileNotFoundError:
            self.game_data = {}

    def save_game_data(self):
        """Save the current game state dictionary into a CSV file."""
        with open(self.file_path, mode="w", newline="") as file:
            fieldnames = ["Name", "Highscore", "Pastgames"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.game_data.values())

    def update_score(self, player_name, new_score):
        """Update a player's high score and past games count."""
        if player_name in self.game_data:
            player = self.game_data[player_name]
            player["Highscore"] = max(int(player["Highscore"]), new_score)
            player["Pastgames"] = int(player["Pastgames"]) + 1
        else:
            self.game_data[player_name] = {"Name": player_name, "Highscore": new_score, "Pastgames": 1}
        self.save_game_data()

    def get_game_data(self):
        """Return the game state dictionary."""
        return self.game_data


class WordleGame:
    """Handles the Wordle gameplay using the BST and game state system."""
    def __init__(self, words_file="./five_letter_words.txt", game_state_file="./game_state.csv"):
        self.word_tree = WordTree()
        self.game_state = GameState(game_state_file)
        self.game_state.load_game_data()
        self.load_words(words_file)

    def load_words(self, file_path):
        """Load words from a file into the BST."""
        try:
            with open(file_path, "r") as file:
                for line in file:
                    self.word_tree.insert(line.strip().lower())
                    print("inserted")
        except FileNotFoundError:
            print("Word file not found.")

    def get_new_word(self):
        """Retrieve a random word from the BST."""
        return self.word_tree.get_random_word()

    def play_round(self, player_name):
        """Simulate a game round and update game state."""
        target_word = self.get_new_word()
        if not target_word:
            print("No words available.")
            return
        
        print(f"New game for {player_name}. Try guessing the word!")
        guessed_word = input("Enter your guess: ").strip().lower()

        if guessed_word == target_word:
            print("Correct! You win!")
            self.game_state.update_score(player_name, 100)  # Example score update
        else:
            print(f"Wrong! The correct word was: {target_word}")
            self.game_state.update_score(player_name, 0)  # No points for wrong guesses



if __name__ == "__main__":
    try:
        print("before the class")
        game = WordleGame()  # Likely point of failure
        print("after the class")
        game.play_round("Alice")
        print("after the round play")
    except Exception as e:
        print(f"Error: {e}")
