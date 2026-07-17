from typing import Dict, Any


class CompanyCache:
    """
    Simple in-memory cache for company data.

    Stores downloaded company information so
    every engine can reuse the same dataset.
    """

    _cache: Dict[str, Any] = {}

    @classmethod
    def has(cls, ticker: str) -> bool:

        return ticker.upper() in cls._cache

    @classmethod
    def get(cls, ticker: str):

        return cls._cache.get(
            ticker.upper()
        )

    @classmethod
    def set(

        cls,

        ticker: str,

        data,

    ):

        cls._cache[
            ticker.upper()
        ] = data

    @classmethod
    def clear(cls):

        cls._cache.clear()