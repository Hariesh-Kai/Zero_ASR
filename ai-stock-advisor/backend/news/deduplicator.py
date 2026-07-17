from difflib import SequenceMatcher


class NewsDeduplicator:
    """
    Removes duplicate or near-duplicate news articles.
    """

    def __init__(self, threshold=0.85):

        self.threshold = threshold

    def _similarity(self, text1, text2):

        return SequenceMatcher(
            None,
            text1.lower(),
            text2.lower(),
        ).ratio()

    def deduplicate(self, articles):

        unique_articles = []

        seen_titles = []

        for article in articles:

            title = article.get(
                "title",
                "",
            )

            duplicate = False

            for existing_title in seen_titles:

                similarity = self._similarity(
                    title,
                    existing_title,
                )

                if similarity >= self.threshold:

                    duplicate = True

                    break

            if not duplicate:

                unique_articles.append(
                    article
                )

                seen_titles.append(
                    title
                )

        return unique_articles