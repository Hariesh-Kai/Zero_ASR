"""
Text Post-Processing and Normalization Module.
Supports two distinct modes:
1. TRANSCRIPTION MODE: Verbatim fidelity, preserves spoken words while applying truecasing and punctuation.
2. CLEAN MODE: Removes disfluencies ('um', 'uh'), stutters, and verbal pauses while strictly preserving meaning.
"""

import re
from typing import List


class TextNormalizer:
    """
    Decoupled text normalizer and truecaser for ASR output.
    Operates on both English and Romanized Tamil without hallucinating tokens.
    """

    # Common English disfluencies / filler vocalizations
    DISFLUENCIES = {
        "um", "uh", "er", "ah", "hmm", "umm", "uhh", "err"
    }

    # Common coordination conjunctions that often demarcate clauses
    CLAUSE_CONNECTORS = {
        "then", "but", "so", "because", "however", "although", "while", "since"
    }

    def __init__(self):
        pass

    def truecase(self, text: str) -> str:
        """
        Applies grammatical capitalization:
        - Capitalizes the initial letter of sentences.
        - Capitalizes standalone 'i' and contractions like 'i'm', 'i'll', 'i'd', 'i've'.
        - Preserves existing capitalization if present.
        """
        if not text:
            return ""

        words = text.split()
        if not words:
            return ""

        # Process words
        processed = []
        capitalize_next = True

        for i, w in enumerate(words):
            low = w.lower()

            # Handle English standalone 'i' or 'i' contractions
            if low == "i":
                w = "I"
            elif low in ("i'm", "i've", "i'll", "i'd"):
                w = "I" + low[1:]

            # If this word is the start of a sentence or utterance
            if capitalize_next and len(w) > 0:
                w = w[0].upper() + w[1:]
                capitalize_next = False

            # Check if this word ends with sentence-terminating punctuation
            if w.endswith((".", "?", "!")):
                capitalize_next = True

            processed.append(w)

        return " ".join(processed)

    def add_punctuation(self, text: str) -> str:
        """
        Lightweight deterministic punctuation heuristic:
        - Adds comma before major clause connectors (e.g. ', then ', ', but ')
        - Ensures utterance terminates with a period (or question mark if inverted/interrogative)
        """
        if not text:
            return ""

        # Normalize spaces
        text = re.sub(r"\s+", " ", text).strip()

        # Add comma before clause connectors if not already preceded by punctuation
        words = text.split()
        punctuated_words = []
        for i, w in enumerate(words):
            low = w.lower()
            if i > 0 and low in self.CLAUSE_CONNECTORS:
                prev = punctuated_words[-1]
                if not prev.endswith((",", ".", "?", "!", ";", ":")):
                    punctuated_words[-1] = prev + ","
            punctuated_words.append(w)

        res = " ".join(punctuated_words)

        # Check for interrogative start (English)
        is_question = False
        first_word = words[0].lower() if words else ""
        if first_word in ("what", "where", "when", "why", "who", "which", "how", "is", "are", "do", "does", "did", "can", "could", "would"):
            is_question = True

        # Ensure terminal punctuation
        if not res.endswith((".", "?", "!")):
            res += "?" if is_question else "."

        return res

    def remove_disfluencies(self, text: str) -> str:
        """
        Removes verbal filler words (um, uh, er) without changing spoken content.
        """
        words = text.split()
        filtered = [w for w in words if w.lower().strip(".,?!") not in self.DISFLUENCIES]
        return " ".join(filtered)

    def remove_stutters(self, text: str) -> str:
        """
        Collapses immediate duplicate words (e.g., 'I I went' -> 'I went').
        """
        words = text.split()
        if not words:
            return ""
        deduped = [words[0]]
        for w in words[1:]:
            if w.lower() != deduped[-1].lower():
                deduped.append(w)
        return " ".join(deduped)

    def process(self, text: str, mode: str = "transcription") -> str:
        """
        Process raw ASR text according to chosen mode:
        - 'transcription': Verbatim with truecasing and punctuation.
        - 'clean': Truecasing, punctuation, plus disfluency and stutter removal.
        """
        text = text.strip()
        if not text:
            return ""

        if mode == "clean":
            text = self.remove_disfluencies(text)
            text = self.remove_stutters(text)

        # Apply clause punctuation
        text = self.add_punctuation(text)

        # Apply truecasing
        text = self.truecase(text)

        return text
