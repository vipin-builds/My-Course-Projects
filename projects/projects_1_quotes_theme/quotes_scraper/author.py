class Author:
    """
    Represents the quoter/author of a quote.

    Attributes:
        name (str): The name of the author.
        bio_link (str): Relative URL to the author's biography page.
        birth_date (str, optional): The author's birth date (fetched later).
        birth_city (str, optional): The author's birth city (fetched later).
    """
    def __init__(self, name, bio_link):
        self.name = name
        self.bio_link = bio_link
        # Initialize attributes that will be fetched later as None/empty
        self.birth_date = None
        self.birth_city = None

    def __repr__(self):
        """
        Developer-focused representation of the Author object.
        Ideally reconstructible and unambiguous.
        """
        if self.birth_date and self.birth_city:
            # Full data representation
            return (f'Author(name="{self.name}", bio_link="{self.bio_link}", '
                    f'birth_date="{self.birth_date}", birth_city="{self.birth_city}")')
        else:
            # Partial data representation (before enrichment)
            return f'Author(name="{self.name}", bio_link="{self.bio_link}")'

    def populate_bio_data(self, birth_date, birth_city):
        """Method to update the author's details once scraped."""
        self.birth_date = birth_date
        self.birth_city = birth_city


