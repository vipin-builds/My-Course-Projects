from quotes_scraper.quotes_scraper import QuotesScraper
from random import choice
import pickle
import os

class GuessQuoteAuthor:

    def __init__(self):
        # Define the scraper here as an instance attribute (self.scraper)
        self.scraper = QuotesScraper("clean")
        self.default_path = "./data/"
        if not os.path.exists(self.default_path):
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            self.default_path = os.path.join(base_dir, "data", "quotes.pickle")
                
        self.pickle_file_path = "".join([self.default_path, "quotes.pickle"])

    def load_quotes_data(self):
        try:
            with open(self.pickle_file_path, "rb") as file:
                quotes_list = pickle.load(file)
        except Exception as err:
            print(f"Pickle file does not exist. {err}")
            print("Running scraper..")
            quotes_list = self.scraper.run_scraper()
            self.scraper.save_quotes(quotes_list)
        finally:
            print("Loaded quotes")

        return quotes_list

    def play_again(self):
        user_want_to_continue = input("Would you like to play again (y/n?) ")
        if user_want_to_continue == "y":
            return True
        else:
            return False

    def generate_hints(self, quote):
        return [f"Author's first name is {quote.author.name.split()[0]}",
            f"Author was born {quote.author.birth_city}", 
            f"Author was born on {quote.author.birth_date}", 
        ]

    def play_game(self, quotes_list):
        #Here is the game logic
        want_to_play = True
        while want_to_play:
            selected_quote = choice(quotes_list)
            self.scraper.populate_author_data(selected_quote)
            hints = self.generate_hints(selected_quote)
            guessed = False

            for tries in range (4, 0,-1):
                if tries == 4:
                    user_guess = input(f"Here is a quote:\n\n{selected_quote.text}\n\nWho said this? Guesses remaining: 4.\n")
                else:
                    print(f"Here's a hint: {hints[tries-1]}")
                    user_guess = input(f"Who said this? Guesses remaining {tries}\n")

                if user_guess != selected_quote.author.name:
                    continue
                else:
                    print("You guessed correctly! Congratulations!")
                    guessed = True
                    break

            if guessed == False:
                print(f"Sorry, you've run out of guesses. The answer was {selected_quote.author.name}\n\n")
            want_to_play = self.play_again()

if __name__ == "__main__":
    # ONLY run this code if the script is the primary program being executed
    game = GuessQuoteAuthor()
    quotes_list = game.load_quotes_data()
    game.play_game(quotes_list)
    
