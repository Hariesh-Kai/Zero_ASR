from technical.indicators.obv import OBVIndicator
from technical.indicators.mfi import MFIIndicator
from technical.indicators.cmf import CMFIndicator
from technical.indicators.vwap import VWAPIndicator


class VolumeAnalyzer:
    """
    Evaluates buying/selling pressure using
    OBV, MFI, CMF and VWAP.
    """

    def __init__(self):

        self.obv = OBVIndicator()

        self.mfi = MFIIndicator()

        self.cmf = CMFIndicator()

        self.vwap = VWAPIndicator()

    def analyze(self, mapped):

        obv = self.obv.latest_value(mapped)

        mfi = self.mfi.latest_value(mapped)

        cmf = self.cmf.latest_value(mapped)

        vwap = self.vwap.latest_value(mapped)

        score = 0

        # MFI
        if 20 <= mfi["value"] <= 80:
            score += 1

        # CMF
        if cmf["signal"] == "Bullish":
            score += 1

        # VWAP
        if vwap["signal"] == "Bullish":
            score += 1

        # OBV
        if obv["value"] > 0:
            score += 1

        if score == 4:

            volume = "Strong Buying"

        elif score == 3:

            volume = "Buying"

        elif score == 2:

            volume = "Neutral"

        elif score == 1:

            volume = "Selling"

        else:

            volume = "Strong Selling"

        confidence = round(
            (score / 4) * 100,
            2,
        )

        return {

            "volume": volume,

            "score": score,

            "max_score": 4,

            "confidence": confidence,

            "obv": obv,

            "mfi": mfi,

            "cmf": cmf,

            "vwap": vwap,
        }