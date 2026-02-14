from .author import Author
from .quotes import Quote
from requests import get
from requests import RequestException
from bs4 import BeautifulSoup
import pickle


class QuotesScraper:
	"""
    A class to retrieve quotes from http://quotes.toscrape.com,
    handle pagination, and return structured Quote objects.
    """
	def __init__(self, load_type="clean"):
		"""Initializes the scraper configuration."""
		self.load_type = load_type
		self.base_url = "http://quotes.toscrape.com"
		self.page = 1

	@property
	def page_url(self):
		"""Dynamically calculates the current page URL based on self.page."""
		return f"{self.base_url}/page/{self.page}/"
		
	def __repr__(self):
		"""Developer-focused representation of the scraper instance."""
		return f"QuotesScraper(load_type='{self.load_type}', current_page={self.page})"

	def get_html_data(self, bio_link=None):
		"""Fetches the raw HTML content for the current page URL."""
		try:
			if bio_link:
				#print(f"Fetching: {bio_link}") # Slightly clearer message
				resp = get(bio_link)
			else:
				#print(f"Fetching: {self.page_url}") # Slightly clearer message
				resp = get(self.page_url)
			resp.raise_for_status()
			data = resp.text # Assign data inside the try block if successful
			#print(f"status: {resp.status_code}") # Use .status_code
			return data # Return here on success
            
		except RequestException as err:
			print(f"Exception occured during API call {err}")
			return None # <--- Explicitly return None on error
            

	def extract_quotes(self, data):
		"""
        Parses HTML data, creates Quote/Author objects for one page, 
        and determines if a next page exists.

        Args:
            data (str): The raw HTML content of the page.

        Returns:
            tuple: (bool more_data_exists, list[Quote] quotes_on_page)
        """
		soup = BeautifulSoup(data, "html.parser")
	
		quotes_divs = soup.find_all("div", class_="quote")
		nav_next = soup.select_one("li.next a") 
		if nav_next:
			more_data = True
			self.page += 1
		else:
			more_data = False

		quotes = []
		for quotes_div in quotes_divs:
			author = Author(quotes_div.small.get_text(), bio_link=f"{self.base_url}{quotes_div.a.attrs.get('href')}")
			quote = Quote(quotes_div.span.get_text(), author)
			quotes.append(quote)

		return more_data, quotes

	def run_scraper(self):
		"""
        Orchestrates the full scraping process across all pages 
        and returns the complete list of Quote objects.
        """
		final_quotes_list = []
		more_data = True
		while more_data:
			data = self.get_html_data()

			if data is None:

				print("Stopping scraper due to data fetch error.")
				break

			more_data, quotes = self.extract_quotes(data)
			final_quotes_list.extend(quotes)

		print(f"\nScraping complete. Total quotes found: {len(final_quotes_list)}")
		return final_quotes_list

	def save_quotes(self, quotes_to_pickle, pickle_file_path):
		print(f"Pickling {len(quotes_to_pickle)} quotes")
		with open(pickle_file_path, "wb") as file:
			pickle.dump(quotes_to_pickle, file)

		print("Pickling complete.")


	def populate_author_data(self, quote):
		author = quote.author
		data = self.get_html_data(author.bio_link)

		if data is None:
			print("Author's bio data fetch error.")
		else:
			soup = BeautifulSoup(data, "html.parser")
	
			birth_date = soup.find("span", class_="author-born-date").get_text()
			birth_location = soup.find("span", class_="author-born-location").get_text()
			author.populate_bio_data(birth_date, birth_location)
