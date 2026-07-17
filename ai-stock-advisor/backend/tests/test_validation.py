import math
import pytest
from conftest import client

TICKERS = [
    "MSFT",
    "AAPL",
    "NVDA",
    "TSLA",
    "JPM",
    "GOOGL",
    "META",
    "AMZN",
    "KO",
    "PEP",
]

@pytest.mark.parametrize("ticker", TICKERS)
def test_scores_are_valid(ticker):

    response = client.get(f"/company/{ticker}")

    assert response.status_code == 200

    analysis = response.json()["analysis"]

    for analyzer, result in analysis.items():

        assert isinstance(result, dict)

        assert "score" in result
        assert "max_score" in result

        score = result["score"]
        max_score = result["max_score"]

        assert isinstance(score, (int, float))
        assert isinstance(max_score, (int, float))

        assert not math.isnan(score)
        assert not math.isnan(max_score)

        assert score >= 0
        assert score <= max_score