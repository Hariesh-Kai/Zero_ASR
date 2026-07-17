from valuation.dcf.assumptions import DCFAssumptions
from valuation.dcf.forecast import RevenueForecast
from valuation.dcf.operating_margin import OperatingMarginForecast
from valuation.dcf.tax import TaxForecast
from valuation.dcf.reinvestment import ReinvestmentForecast
from valuation.dcf.free_cash_flow import FreeCashFlowForecast
from valuation.dcf.wacc import WACC
from valuation.dcf.discount import DiscountCashFlow
from valuation.dcf.terminal import TerminalValue
from valuation.dcf.present_value import PresentValue
from valuation.dcf.enterprise_value import EnterpriseValue
from valuation.dcf.equity import EquityValue
from valuation.dcf.report import DCFReport
class ProfessionalDCF:

    def __init__(self):

        self.assumptions = DCFAssumptions()

        self.forecast = RevenueForecast()

        self.margin = OperatingMarginForecast()

        self.tax = TaxForecast()

        self.reinvestment = ReinvestmentForecast()

        self.fcf = FreeCashFlowForecast()

        self.wacc = WACC()

        self.discount = DiscountCashFlow()

        self.terminal = TerminalValue()

        self.present_value = PresentValue()

        self.enterprise = EnterpriseValue()

        self.equity = EquityValue()

        self.report = DCFReport()

    def value(

        self,

        company,

        financials,

    ):

        assumptions = self.assumptions.get()

        revenues = self.forecast.forecast(

            financials["income_statement"]["revenue"],

            assumptions,

        )

        ebit = self.margin.forecast(

            revenues,

            assumptions,

        )

        nopat = self.tax.forecast(

            ebit,

            assumptions,

        )

        reinvestment = self.reinvestment.forecast(

            revenues,

            financials["income_statement"]["revenue"],

            assumptions,

        )

        fcf = self.fcf.forecast(

            nopat,

            reinvestment,

        )

        wacc = self.wacc.calculate(

            assumptions,

        )

        discounted_fcf = self.discount.discount(

            fcf,

            wacc,

        )

        terminal = self.terminal.calculate(

            fcf[-1],

            assumptions,

            wacc,

        )

        discounted_terminal = self.present_value.calculate(

            terminal,

            assumptions,

            wacc,

        )

        enterprise_value = self.enterprise.calculate(

            discounted_fcf,

            discounted_terminal,

        )

        

        equity = self.equity.calculate(

            enterprise_value,

            company,

        )

        return self.report.build(

            company=company,

            assumptions=assumptions,

            revenues=revenues,

            ebit=ebit,

            nopat=nopat,

            reinvestment=reinvestment,

            fcf=fcf,

            wacc=wacc,

            discounted_fcf=discounted_fcf,

            terminal=terminal,

            discounted_terminal=discounted_terminal,

            enterprise_value=enterprise_value,

            equity=equity,

        )