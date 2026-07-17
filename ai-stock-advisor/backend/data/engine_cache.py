from typing import Any, Dict


class EngineCache:
    """
    Stores analysis results for each engine.

    Example:

    {
        "MSFT": {
            "fundamental": {...},
            "technical": {...},
            "valuation": {...},
            "news": {...},
            "advisor": {...},
        }
    }
    """

    _cache: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def has(
        cls,
        ticker: str,
        engine: str,
    ) -> bool:

        ticker = ticker.upper()

        return (
            ticker in cls._cache
            and engine in cls._cache[ticker]
        )

    @classmethod
    def get(
        cls,
        ticker: str,
        engine: str,
    ):

        ticker = ticker.upper()

        return cls._cache[ticker][engine]

    @classmethod
    def set(
        cls,
        ticker: str,
        engine: str,
        data,
    ):

        ticker = ticker.upper()

        if ticker not in cls._cache:

            cls._cache[ticker] = {}

        cls._cache[ticker][engine] = data

    @classmethod
    def clear(cls):

        cls._cache.clear()

    @classmethod
    def clear_ticker(
        cls,
        ticker: str,
    ):

        ticker = ticker.upper()

        cls._cache.pop(
            ticker,
            None,
        )