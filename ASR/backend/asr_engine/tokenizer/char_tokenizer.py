"""
Unified Latin Character Tokenizer for English and Romanized Tamil.
Supports CTC Blank (id 0), Unknown (id 1), Space, Apostrophe, a-z, and Language Tags.
"""

import json
from pathlib import Path
from typing import List, Dict, Union


class CharTokenizer:
    """
    Compact character-level tokenizer mapping Latin characters to integer token IDs.
    CTC requires index 0 to be reserved for <blank>.
    """
    BLANK = "<blank>"
    UNK = "<unk>"
    SPACE = " "
    TAG_EN = "<en>"
    TAG_TA = "<ta>"

    def __init__(self, custom_chars: List[str] = None):
        # 0: <blank>, 1: <unk>, 2: ' ', 3: "'", 4: '<en>', 5: '<ta>'
        # Followed by 'a' through 'z'
        base_tokens = [
            self.BLANK,
            self.UNK,
            self.SPACE,
            "'",
            self.TAG_EN,
            self.TAG_TA,
        ]
        alpha_tokens = [chr(c) for c in range(ord('a'), ord('z') + 1)]
        
        if custom_chars:
            extra = [c for c in custom_chars if c not in base_tokens and c not in alpha_tokens]
        else:
            extra = []

        self.vocab: List[str] = base_tokens + alpha_tokens + extra
        self.token2id: Dict[str, int] = {t: i for i, t in enumerate(self.vocab)}
        self.id2token: Dict[int, str] = {i: t for i, t in enumerate(self.vocab)}
        
        self.blank_id = self.token2id[self.BLANK]
        self.unk_id = self.token2id[self.UNK]
        self.space_id = self.token2id[self.SPACE]

    def __len__(self) -> int:
        return len(self.vocab)

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)

    def normalize_text(self, text: str) -> str:
        """
        Normalize text to standard Latin lowercase, trimming extra whitespaces.
        Preserves apostrophes for contractions (e.g., don't, i'm).
        """
        text = text.lower().strip()
        # Replace multiple spaces with a single space
        import re
        text = re.sub(r"\s+", " ", text)
        return text

    def encode(self, text: str, add_lang_tag: str = None) -> List[int]:
        """
        Convert string into list of token IDs.
        """
        text = self.normalize_text(text)
        token_ids: List[int] = []

        if add_lang_tag:
            tag_id = self.token2id.get(add_lang_tag)
            if tag_id is not None:
                token_ids.append(tag_id)

        for char in text:
            token_ids.append(self.token2id.get(char, self.unk_id))

        return token_ids

    def decode(self, token_ids: List[int], remove_special: bool = True) -> str:
        """
        Decode a list of token IDs back into string.
        """
        chars = []
        for tid in token_ids:
            if tid == self.blank_id:
                continue
            token = self.id2token.get(tid, "")
            if remove_special and token in (self.BLANK, self.UNK, self.TAG_EN, self.TAG_TA):
                continue
            chars.append(token)
        return "".join(chars)

    def save(self, path: Union[str, Path]) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"vocab": self.vocab}, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: Union[str, Path]) -> "CharTokenizer":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        inst = cls()
        inst.vocab = data["vocab"]
        inst.token2id = {t: i for i, t in enumerate(inst.vocab)}
        inst.id2token = {i: t for i, t in enumerate(inst.vocab)}
        inst.blank_id = inst.token2id[cls.BLANK]
        inst.unk_id = inst.token2id[cls.UNK]
        inst.space_id = inst.token2id[cls.SPACE]
        return inst
