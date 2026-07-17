class NewsImpactAnalyzer:
    """
    Determines the importance of a news article
    based on its classified category.
    """

    IMPACT_TABLE = {

        "Earnings": {
            "impact": "Very High",
            "score": 95,
            "reason": "Quarterly earnings directly affect company valuation."
        },

        "Merger & Acquisition": {
            "impact": "Very High",
            "score": 95,
            "reason": "Mergers and acquisitions can significantly change company value."
        },

        "Executive Change": {
            "impact": "Very High",
            "score": 90,
            "reason": "Leadership changes often influence investor confidence."
        },

        "Lawsuit": {
            "impact": "High",
            "score": 85,
            "reason": "Legal issues may affect financial performance."
        },

        "Macro Economy": {
            "impact": "High",
            "score": 85,
            "reason": "Macroeconomic events influence the entire market."
        },

        "Dividend": {
            "impact": "High",
            "score": 80,
            "reason": "Dividend announcements influence shareholder returns."
        },

        "AI": {
            "impact": "Medium",
            "score": 65,
            "reason": "AI developments can influence future business growth."
        },

        "Chip": {
            "impact": "Medium",
            "score": 65,
            "reason": "Semiconductor developments can affect technology companies."
        },

        "Product Launch": {
            "impact": "Medium",
            "score": 60,
            "reason": "New products may improve future revenue."
        },

        "Partnership": {
            "impact": "Medium",
            "score": 55,
            "reason": "Strategic partnerships may support long-term growth."
        },

        "General": {
            "impact": "Low",
            "score": 30,
            "reason": "General news usually has limited impact on valuation."
        }
    }

    def analyze(self, classification):

        category = classification["category"]

        return self.IMPACT_TABLE.get(
            category,
            self.IMPACT_TABLE["General"]
        )