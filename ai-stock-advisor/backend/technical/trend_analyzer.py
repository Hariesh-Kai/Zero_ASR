from technical.indicators.sma import SMAIndicator
from technical.indicators.ema import EMAIndicator
from technical.indicators.macd import MACDIndicator
from technical.indicators.adx import ADXIndicator


class TrendAnalyzer:
    """
    Determines the market trend using
    SMA, EMA, MACD and ADX.
    Uses a weighted scoring model (100 points).
    """

    EMA_ALIGNMENT_WEIGHT = 30
    PRICE_POSITION_WEIGHT = 25
    MACD_WEIGHT = 20
    ADX_WEIGHT = 15
    SMA_ALIGNMENT_WEIGHT = 10

    def __init__(self):

        self.sma = SMAIndicator()

        self.ema = EMAIndicator()

        self.macd = MACDIndicator()

        self.adx = ADXIndicator()

    def analyze(self, mapped):

        sma20 = self.sma.latest_value(
            mapped,
            20,
        )

        sma50 = self.sma.latest_value(
            mapped,
            50,
        )

        ema20 = self.ema.latest_value(
            mapped,
            20,
        )

        ema50 = self.ema.latest_value(
            mapped,
            50,
        )

        macd = self.macd.latest_value(
            mapped,
        )

        adx = self.adx.latest_value(
            mapped,
        )

        close = mapped.iloc[-1]["close"]

        trend_score = 0

        # ---------------------------------------
        # EMA Alignment (30)
        # ---------------------------------------

        if ema20["value"] > ema50["value"]:

            trend_score += self.EMA_ALIGNMENT_WEIGHT

        # ---------------------------------------
        # Price Position (25)
        # ---------------------------------------

        price_points = self.PRICE_POSITION_WEIGHT / 4

        if close > ema20["value"]:

            trend_score += price_points

        if close > ema50["value"]:

            trend_score += price_points

        if close > sma20["value"]:

            trend_score += price_points

        if close > sma50["value"]:

            trend_score += price_points

        # ---------------------------------------
        # MACD Confirmation (20)
        # ---------------------------------------

        if macd["signal"] == "Bullish":

            trend_score += self.MACD_WEIGHT

        # ---------------------------------------
        # ADX Strength (15)
        # ---------------------------------------

        adx_value = adx["value"]

        if adx_value >= 40:

            trend_score += 15

        elif adx_value >= 25:

            trend_score += 10

        elif adx_value >= 20:

            trend_score += 5

        # ---------------------------------------
        # SMA Alignment (10)
        # ---------------------------------------

        if sma20["value"] > sma50["value"]:

            trend_score += self.SMA_ALIGNMENT_WEIGHT

        trend_score = round(
            trend_score,
            2,
        )

        # ---------------------------------------
        # Trend Classification
        # ---------------------------------------

        if trend_score >= 85:

            trend = "Strong Bullish"

            strength = "Very Strong"

        elif trend_score >= 70:

            trend = "Bullish"

            strength = "Strong"

        elif trend_score >= 50:

            trend = "Neutral"

            strength = "Moderate"

        elif trend_score >= 30:

            trend = "Bearish"

            strength = "Weak"

        else:

            trend = "Strong Bearish"

            strength = "Very Weak"

        # ---------------------------------------
        # Grade
        # ---------------------------------------

        if trend_score >= 90:

            grade = "A+"

        elif trend_score >= 80:

            grade = "A"

        elif trend_score >= 70:

            grade = "B"

        elif trend_score >= 60:

            grade = "C"

        elif trend_score >= 50:

            grade = "D"

        else:

            grade = "F"

        # ---------------------------------------
        # Summary
        # ---------------------------------------

        summary = (
            f"Trend is {trend.lower()}. "
            f"EMA alignment, moving averages, "
            f"MACD confirmation and ADX trend "
            f"strength produced a score of "
            f"{trend_score}/100."
        )

        return {

            "trend": trend,

            "strength": strength,

            "trend_score": trend_score,

            "grade": grade,

            "confidence": trend_score,

            "summary": summary,

            "sma20": sma20,

            "sma50": sma50,

            "ema20": ema20,

            "ema50": ema50,

            "macd": macd,

            "adx": adx,
        }