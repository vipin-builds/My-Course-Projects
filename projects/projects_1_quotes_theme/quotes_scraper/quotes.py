from .author import Author

class Quote:
    """
    Represents a single quote and its associated author.
    """
    def __init__(self, text, author_obj: Author):
        self.text = text
        self.author = author_obj # <-- This is the nested object/composition

    def __repr__(self):
        """
        Developer-focused representation of the Quote object.
        It explicitly calls repr() on the nested author object.
        """
        # We explicitly call repr() on the nested author object for full debug info
        return f'Quote(text="{self.text}", author_obj={repr(self.author)})'

    
    def __str__(self):
        """User-friendly print representation."""
        return f"{self.text} - {self.author.name}"