class GrowthRatios:
    """
    Growth ratio calculations.
    """

    @staticmethod
    def growth_rate(current, previous):
        if current is None or previous is None:
            return None

        if previous == 0:
            return None

        return ((current - previous) / abs(previous)) * 100

    @staticmethod
    def revenue_growth(current_revenue, previous_revenue):
        return GrowthRatios.growth_rate(
            current_revenue,
            previous_revenue,
        )

    @staticmethod
    def earnings_growth(current_income, previous_income):
        return GrowthRatios.growth_rate(
            current_income,
            previous_income,
        )

    @staticmethod
    def eps_growth(current_eps, previous_eps):
        return GrowthRatios.growth_rate(
            current_eps,
            previous_eps,
        )

    @staticmethod
    def cashflow_growth(current_cashflow, previous_cashflow):
        return GrowthRatios.growth_rate(
            current_cashflow,
            previous_cashflow,
        )