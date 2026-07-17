class BaseAnalyzer:
    """
    Base class for all analyzers.
    Provides a standardized response format.
    """

    @staticmethod
    def build_result(
        score,
        max_score,
        quality,
        metrics=None,
        summary=None,
    ):
        return {
            "score": score,
            "max_score": max_score,
            "quality": quality,
            "metrics": metrics or {},
            "summary": summary,
        }