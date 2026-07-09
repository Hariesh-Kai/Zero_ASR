class ProfitabilityScore:

    @staticmethod
    def score(roe, roa, roce, net_margin):

        score = 0

        # ROE (30 points)
        if roe is not None:
            if roe >= 20:
                score += 30
            elif roe >= 15:
                score += 25
            elif roe >= 10:
                score += 15
            else:
                score += 5

        # ROA (20 points)
        if roa is not None:
            if roa >= 10:
                score += 20
            elif roa >= 7:
                score += 15
            elif roa >= 5:
                score += 10
            else:
                score += 5

        # ROCE (30 points)
        if roce is not None:
            if roce >= 20:
                score += 30
            elif roce >= 15:
                score += 25
            elif roce >= 10:
                score += 15
            else:
                score += 5

        # Net Margin (20 points)
        if net_margin is not None:
            if net_margin >= 20:
                score += 20
            elif net_margin >= 10:
                score += 15
            elif net_margin >= 5:
                score += 10
            else:
                score += 5

        return score