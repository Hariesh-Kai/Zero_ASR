class BeneishRatios:
    """
    Beneish M-Score calculations.

    Reference:
    Messod D. Beneish (1999)
    """

    @staticmethod
    def dsri(
        receivables,
        previous_receivables,
        revenue,
        previous_revenue,
    ):
        if (
            None in (
                receivables,
                previous_receivables,
                revenue,
                previous_revenue,
            )
            or revenue == 0
            or previous_revenue == 0
        ):
            return None

        return (
            (receivables / revenue)
            /
            (previous_receivables / previous_revenue)
        )

    @staticmethod
    def gmi(
        revenue,
        gross_profit,
        previous_revenue,
        previous_gross_profit,
    ):
        if (
            None in (
                revenue,
                gross_profit,
                previous_revenue,
                previous_gross_profit,
            )
        ):
            return None

        if revenue == 0 or previous_revenue == 0:
            return None

        current_margin = gross_profit / revenue
        previous_margin = previous_gross_profit / previous_revenue

        if current_margin == 0:
            return None

        return previous_margin / current_margin

    @staticmethod
    def aqi(
        total_assets,
        current_assets,
        ppe,
        previous_assets,
        previous_current_assets,
        previous_ppe,
    ):
        if None in (
            total_assets,
            current_assets,
            ppe,
            previous_assets,
            previous_current_assets,
            previous_ppe,
        ):
            return None

        if total_assets == 0 or previous_assets == 0:
            return None

        current = (
            1 -
            (
                current_assets + ppe
            ) / total_assets
        )

        previous = (
            1 -
            (
                previous_current_assets + previous_ppe
            ) / previous_assets
        )

        if previous == 0:
            return None

        return current / previous

    @staticmethod
    def sgi(
        revenue,
        previous_revenue,
    ):
        if (
            revenue is None
            or previous_revenue in (None, 0)
        ):
            return None

        return revenue / previous_revenue

    @staticmethod
    def m_score(
        dsri,
        gmi,
        aqi,
        sgi,
    ):
        if None in (
            dsri,
            gmi,
            aqi,
            sgi,
        ):
            return None

        return (
            -4.84
            + 0.92 * dsri
            + 0.528 * gmi
            + 0.404 * aqi
            + 0.892 * sgi
        )