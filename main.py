from random import choice
import csv


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

    def load_words(self, file_path, limit=40):
        """Load words from a file into the BST, stopping after a specified limit."""
        try:
            with open(file_path, "r") as file:
                count = 0
                for line in file:
                    if count >= limit:
                        break
                    self.word_tree.insert(line.strip().lower())
                    count += 1
        except FileNotFoundError:
            print("Word file not found.")


    def get_new_word(self):
        """Retrieve a random word from the BST."""
        return self.word_tree.get_random_word()
    
    def display_letter_panel(self, letter_status):
        """Display letter status panel showing green, yellow, and unused letters."""
        import string
        print("\nLetter Panel:")
        panel = ""
        for letter in string.ascii_lowercase:
            status = letter_status.get(letter, "unused")
            if status == "green":
                panel += f"[{letter.upper()}] "
            elif status == "yellow":
                panel += f"({letter.upper()}) " 
            elif status == "unused":
                panel += f" {letter.upper()}  " 

        print(panel + "\n")

    def play_round(self, player_name):
        """Simulate a game round and update game state."""
        target_word = self.get_new_word()
        if not target_word:
            print("No words available.")
            return
        
        print(f"New game for {player_name}. Try guessing the word!")
        attempts = 4
        
        import string
        letter_status = {letter: "unused" for letter in string.ascii_lowercase}

        for attempt in range(1, attempts + 1):
            guess_word = input(f"Attempt {attempt}/{attempts} - Enter your guess: ").strip().lower()
            
            if len(guess_word) != 5:
                print("Invalid input. Please enter exactly 5 letters.")
                continue

            if guess_word == target_word:
                print("Correct! You win!")
                score = 100 - (attempt - 1) * 25
                self.game_state.update_score(player_name, score)
                break
            
            feedback = ["_"] * 5
            used_indices = []

            for i in range(5):
                if guess_word[i] == target_word[i]:
                    feedback[i] = f"[{guess_word[i].upper()}]"
                    used_indices.append(i)
                    
            for i in range(5):
                if feedback[i] == "_":
                    for j in range(5):
                        if j not in used_indices and guess_word[i] == target_word[j]:
                            feedback[i] = f"({guess_word[i].upper()})"
                            used_indices.append(j)
                            break

            for i in range(5):
                letter = guess_word[i]
                if feedback[i].startswith("["):
                    letter_status[letter] = "green"
                elif feedback[i].startswith("("):
                    if letter_status[letter] != "green":
                        letter_status[letter] = "yellow"
                else:
                    if letter_status[letter] not in ["green", "yellow"]:
                        letter_status[letter] = "gray"

            print("Feedback:", " ".join(feedback))
            self.display_letter_panel(letter_status)
            print()

            if attempt == attempts:
                print(f"Game over! The word was: {target_word}")





if __name__ == "__main__":
    try:
        game = WordleGame() 
        game.play_round("Alice")
    except Exception as e:
        print(f"Error: {e}")
