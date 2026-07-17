from ai.strengths import StrengthAnalyzer
from ai.risks import RiskAnalyzer
from ai.verdict import VerdictGenerator


class AISummary:

    def __init__(self):
        self.strengths = StrengthAnalyzer()
        self.risks = RiskAnalyzer()
        self.verdict = VerdictGenerator()

    def generate(
        self,
        analysis,
        scores,
        recommendation,
    ):

        strengths = self.strengths.generate(
            analysis,
            scores,
        )

        risks = self.risks.generate(
            analysis,
            scores,
        )

        verdict = self.verdict.generate(
            strengths,
            risks,
            recommendation,
        )

        return {
            "strengths": strengths,
            "risks": risks,
            "verdict": verdict,
        }