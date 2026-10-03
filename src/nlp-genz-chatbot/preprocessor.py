import re


class TextPreprocessor:
    """Regex-based text normalization."""

    def normalize(self, text):
        text = text.lower()
        text = re.sub(r"\bfront[\s-]end\b", "frontend", text)
        text = re.sub(r"\bback[\s-]end\b", "backend", text)
        text = re.sub(r"'s\b", "", text)       # what's -> what
        text = text.replace("'", "")           # don't -> dont
        text = re.sub(r"(.)\1{2,}", r"\1\1", text)  # sooo -> soo
        text = re.sub(r"[^a-z0-9\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip()
