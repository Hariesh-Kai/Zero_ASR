from datetime import datetime


class NewsAnalyzer:
    """
    Converts raw provider news into a
    standardized format.
    """

    def analyze(self, articles):

        normalized = []

        for article in articles:

            content = article.get("content", {})

            provider = content.get(
                "provider",
                {},
            )

            canonical = content.get(
                "canonicalUrl",
                {},
            )

            normalized.append(

                {

                    "id": article.get("id"),

                    "title": content.get(
                        "title"
                    ),

                    "description": content.get(
                        "description"
                    ),

                    "summary": content.get(
                        "summary"
                    ),

                    "published": content.get(
                        "pubDate"
                    ),

                    "publisher": provider.get(
                        "displayName"
                    ),

                    "url": canonical.get(
                        "url"
                    ),

                    "content_type": content.get(
                        "contentType"
                    ),

                }

            )

        return normalized