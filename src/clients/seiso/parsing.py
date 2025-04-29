
from typing import (
    Any,
    List,
    Dict,
)
from ..postgredb import PostgreDatabaseClient
from sqlalchemy import func

from seisoparser import ParserResult, WordCategories  # External package
from spetekmyo import Root, GrammaticalCategories


class SeisoParserClient:
    """
    Lets you parse words in the Seiso language,
    based on grammatical components hosted online in the Seiso dictionnary.
    
    IMPORTANT : This object caches the words requested from the Seiso database by default.
    You can clear this cache manually (so that it gets updated) or disable it altogether in the constructor.
    """
    def __init__(self, seiso_db_client: PostgreDatabaseClient, use_cache = True):
        """
        Parameters:
            seiso_db_client (DatabaseClient):
                A connection to an online database supporting the "spetekmyo" module, 
                which can provide roots and their grammatical types. 
            use_cache (bool):
                Set to False to disable using the cache.
                If the cache is active, it must be cleared manually using the method
                .clear_cache() so that the words are refreshed the next time a parsing is attempted.
        """
        self.seiso_db_client = seiso_db_client
        self.use_cache = use_cache
        self._cached_roots: WordCategories = None

    def get_roots(self) -> WordCategories:

        with self.seiso_db_client.handler() as session:
            query = session.query(
                Root.grammatical_category,
                func.array_agg(Root.label).label("label_values")
            ).group_by(Root.grammatical_category)

            # Build the dictionary from the result
            result: Dict[GrammaticalCategories, List[str]] = {row.grammatical_category: row.label_values for row in query.all()}
            return WordCategories(
                initials=result.get("initial", []),
                finals=result.get("final", []),
                numerals=result.get("numeral", []),
                placeholders=result.get("mixed", []),
            )

    @property
    def roots(self):
        if self._cached_roots is None or self.use_cache is False:
            self._cached_roots = self.get_roots()
        return self._cached_roots

    def clear_cache(self):
        """
        Schedule the roots to be recomputed 
        next time you try to parse a word.
        """
        self._cached_roots = None

    def parse(self, input: str) -> ParserResult:
        return ParserResult.from_string(inp=input, word_categories=self.roots)
