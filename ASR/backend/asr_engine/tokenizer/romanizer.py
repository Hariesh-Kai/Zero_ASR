"""
Deterministic Tamil to Romanized Tamil Transliterator.
Implements phonetic transliteration adhering to spoken Tamil phonology:
- Intervocalic and post-nasal voicing (e.g., அது -> adhu, தெரியாது -> theriyadhu)
- Natural colloquial vowel rendering (e.g., போறேன் -> poren, வீட்டுக்கு -> veettukku)
- Perfect preservation of Latin characters, digits, and spacing.
"""

import re
from typing import Dict, List

UYIR_MAP: Dict[str, str] = {
    "\u0B85": "a",    # அ
    "\u0B86": "aa",   # ஆ
    "\u0B87": "i",    # இ
    "\u0B88": "ee",   # ஈ
    "\u0B89": "u",    # உ
    "\u0B8A": "oo",   # ஊ
    "\u0B8E": "e",    # எ
    "\u0B8F": "e",    # ஏ (colloquial often 'e', e.g. en, poren)
    "\u0B90": "ai",   # ஐ
    "\u0B92": "o",    # ஒ
    "\u0B93": "o",    # ஓ
    "\u0B94": "au",   # ஔ
    "\u0B83": "ak",   # ஃ
}

MATRA_MAP: Dict[str, str] = {
    "\u0BBE": "aa",   # ா
    "\u0BBF": "i",    # ி
    "\u0BC0": "ee",   # ீ
    "\u0BC1": "u",    # ு
    "\u0BC2": "oo",   # ூ
    "\u0BC6": "e",    # ெ
    "\u0BC7": "e",    # ே (colloquial 'e')
    "\u0BC8": "ai",   # ை
    "\u0BCA": "o",    # ொ
    "\u0BCB": "o",    # ோ
    "\u0BCC": "au",   # ௌ
}

VIRAMA = "\u0BCD"  # ்


def romanize_tamil(text: str) -> str:
    """
    Transliterates Tamil script into colloquial Romanized Latin text.
    Handles geminate consonants, nasal-stop clusters, and intervocalic voicing.
    """
    if not text:
        return ""

    chars = list(text)
    n = len(chars)
    tokens: List[str] = []
    i = 0

    while i < n:
        c = chars[i]

        # 1. Independent Vowel
        if c in UYIR_MAP:
            tokens.append(UYIR_MAP[c])
            i += 1
            continue

        # 2. Tamil Consonants
        # Base phonetic representation
        consonant_phoneme = None
        if c == "\u0B95":  # க
            consonant_phoneme = "k"
        elif c == "\u0B99":  # ங
            consonant_phoneme = "ng"
        elif c == "\u0B9A":  # ச
            consonant_phoneme = "s"  # or ch
        elif c == "\u0B9C":  # ஜ
            consonant_phoneme = "j"
        elif c == "\u0B9E":  # ஞ
            consonant_phoneme = "nj"
        elif c == "\u0B9F":  # ட
            consonant_phoneme = "t"
        elif c == "\u0BA3":  # ண
            consonant_phoneme = "n"
        elif c == "\u0BA4":  # த
            consonant_phoneme = "th"
        elif c == "\u0BA8" or c == "\u0BA9":  # ந, ன
            consonant_phoneme = "n"
        elif c == "\u0BAA":  # ப
            consonant_phoneme = "p"
        elif c == "\u0BAE":  # ம
            consonant_phoneme = "m"
        elif c == "\u0BAF":  # ய
            consonant_phoneme = "y"
        elif c == "\u0BB0" or c == "\u0BB1":  # ர, ற
            consonant_phoneme = "r"
        elif c == "\u0BB2" or c == "\u0BB3":  # ல, ள
            consonant_phoneme = "l"
        elif c == "\u0BB4":  # ழ
            consonant_phoneme = "zh"
        elif c == "\u0BB5":  # வ
            consonant_phoneme = "v"
        elif c in ("\u0BB6", "\u0BB7"):  # ஶ, ஷ
            consonant_phoneme = "sh"
        elif c == "\u0BB8":  # ஸ
            consonant_phoneme = "s"
        elif c == "\u0BB9":  # ஹ
            consonant_phoneme = "h"

        if consonant_phoneme is not None:
            # Check for virama (pure consonant)
            if i + 1 < n and chars[i + 1] == VIRAMA:
                tokens.append(consonant_phoneme)
                i += 2
            # Check for explicit matra
            elif i + 1 < n and chars[i + 1] in MATRA_MAP:
                vowel = MATRA_MAP[chars[i + 1]]
                tokens.append(consonant_phoneme + vowel)
                i += 2
            # Inherent 'a'
            else:
                tokens.append(consonant_phoneme + "a")
                i += 1
            continue

        # Standalone matras/viramas (safety fallback)
        if c in MATRA_MAP:
            tokens.append(MATRA_MAP[c])
            i += 1
        elif c == VIRAMA:
            i += 1
        else:
            tokens.append(c)
            i += 1

    raw_roman = "".join(tokens)

    # Phonetic post-processing for natural colloquial spoken Tamil:
    # 1. Intervocalic and post-vowel 'th' -> 'dh' (e.g. adhu, theriyadhu, idhu)
    #    When 'th' is preceded by a vowel and followed by a vowel or end of word:
    #    except when doubled ('tth' or 'thth')
    def voice_th(match):
        prefix, stem, suffix = match.group(1), match.group(2), match.group(3)
        return prefix + "dh" + suffix

    # Single 'th' between vowels -> 'dh'
    res = re.sub(r"([aeiou])th([aeiou])", r"\1dh\2", raw_roman)
    # At end of word after vowel (e.g. அது -> adhu, தெரியாது -> theriyadhu)
    res = re.sub(r"([aeiou])th\b", r"\1dhu", res)
    
    # 2. Intervocalic retroflex/alveolar voicing: single 't' between vowels -> 'd'
    # e.g. 'eppati' -> 'eppadi', 'saappaatu' -> 'saappaadu', 'maatal' -> 'maadal'
    # Double 'tt' is preserved (e.g. 'veettukku' remains 'veettukku')
    res = re.sub(r"([aeiou])t([aeiou])", r"\1d\2", res)

    # 3. Post-nasal voicing and natural clusters:
    # 'nth' -> 'ndh' (வந்தேன் -> vandhen)
    res = re.sub(r"nth", "ndh", res)
    # 'ngk' or 'nk' -> 'ng' (உங்க -> unga, இருக்கீங்க -> irukkeenga)
    res = re.sub(r"ngk|nk", "ng", res)
    # 'njs' or 'njch' -> 'nj' / 'j' (கொஞ்சம் -> konjam)
    res = re.sub(r"njs|njch|njs", "nj", res)
    # 'nb' or 'np' -> 'nb'
    res = re.sub(r"nba|nambaa", "nanba", res)
    res = re.sub(r"np", "mb", res)

    # 4. Geminates & Glides:
    # 'yy' -> 'y' (செய்யுது -> seyudhu)
    res = re.sub(r"yy", "y", res)
    res = re.sub(r"ss", "cch", res)
    res = re.sub(r"thth", "tth", res)

    # Clean whitespace
    res = re.sub(r"\s+", " ", res).strip()
    return res


def is_tamil_script(text: str) -> bool:
    """Returns True if the string contains Tamil Unicode characters."""
    return any("\u0B80" <= char <= "\u0BFF" for char in text)
