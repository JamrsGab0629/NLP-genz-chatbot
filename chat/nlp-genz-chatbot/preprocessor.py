import re


class TextPreprocessor:
    """Regex-based text normalization."""

    def normalize(self, text):
        text = text.lower()
        # collapse 3+ repeated letters: "sooo" -> "so"
        text = re.sub(r"(.)\1{2,}", r"\1\1", text)
        # remove punctuation (keep letters, digits, spaces)
        text = re.sub(r"[^a-z0-9\s]", " ", text)
      
        text = re.sub(r"\s+", " ", text).strip()
        return text
