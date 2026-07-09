class ValuationScore:
    """
    Scores valuation metrics.
    Maximum Score: 100
    """

    @staticmethod
    def score(
        pe_ratio,
        pb_ratio,
        ps_ratio,
        ev_to_ebitda,
        peg_ratio=None,
    ):

        score = 0

        # ---------------------------------
        # PE Ratio (25)
        # ---------------------------------
        if pe_ratio is not None:
            if pe_ratio <= 15:
                score += 25
            elif pe_ratio <= 25:
                score += 20
            elif pe_ratio <= 35:
                score += 15
            else:
                score += 5

        # ---------------------------------
        # PB Ratio (20)
        # ---------------------------------
        if pb_ratio is not None:
            if pb_ratio <= 2:
                score += 20
            elif pb_ratio <= 4:
                score += 15
            elif pb_ratio <= 8:
                score += 10
            else:
                score += 5

        # ---------------------------------
        # PS Ratio (20)
        # ---------------------------------
        if ps_ratio is not None:
            if ps_ratio <= 2:
                score += 20
            elif ps_ratio <= 5:
                score += 15
            elif ps_ratio <= 10:
                score += 10
            else:
                score += 5

        # ---------------------------------
        # EV / EBITDA (20)
        # ---------------------------------
        if ev_to_ebitda is not None:
            if ev_to_ebitda <= 10:
                score += 20
            elif ev_to_ebitda <= 15:
                score += 15
            elif ev_to_ebitda <= 20:
                score += 10
            else:
                score += 5

        # ---------------------------------
        # PEG Ratio (15)
        # ---------------------------------
        if peg_ratio is not None:
            if peg_ratio <= 1:
                score += 15
            elif peg_ratio <= 2:
                score += 10
            elif peg_ratio <= 3:
                score += 5

        return score