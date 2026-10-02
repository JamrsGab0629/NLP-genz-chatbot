import re
import math
import random
from collections import Counter

from preprocessor import TextPreprocessor
from constants import STOP_WORDS, INTENT_DATABASE, GEN_Z_SLANG, GEN_Z_KEYWORDS


class NLPEngine:
    def __init__(self, similarity_threshold=0.12):
        self.preprocessor = TextPreprocessor()
        self.stop_words = STOP_WORDS
        self.intent_database = INTENT_DATABASE
        self.gen_z_slang = GEN_Z_SLANG
        self.similarity_threshold = similarity_threshold

        # Longest first, so "no cap" is matched before "cap"
        keywords = sorted(GEN_Z_KEYWORDS, key=len, reverse=True)
        self.slang_pattern = re.compile(
            r"\b(?:" + "|".join(re.escape(k) for k in keywords) + r")\b",
            re.IGNORECASE,
        )
        self.dumbel_pattern = re.compile(r"\bdumbel+s?\b", re.IGNORECASE)

    def tokenize(self, text):
        """Normalizes text, extracts tokens, and removes stop words."""
        clean_text = self.preprocessor.normalize(text)
        words = re.findall(r"\b\w+\b", clean_text)
        return [w for w in words if w not in self.stop_words]

    def text_to_vector(self, text):
        return Counter(self.tokenize(text))

    def cosine_similarity(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum(vec1[x] * vec2[x] for x in intersection)

        sum1 = sum(v ** 2 for v in vec1.values())
        sum2 = sum(v ** 2 for v in vec2.values())
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        return float(numerator) / denominator

    def detect_user_slang(self, text):
        matches = [m.lower() for m in self.slang_pattern.findall(text)]
        return list(dict.fromkeys(matches))  # removes duplicates, keeps order

    def get_response(self, user_input):
        if self.dumbel_pattern.search(user_input):
            return random.choice(self.gen_z_slang["easter_egg_dumbel"])

        user_vec = self.text_to_vector(user_input)

        if not user_vec:
            return random.choice(self.gen_z_slang["scope_violation"])

        detected_slang = self.detect_user_slang(user_input)

        best_intent = None
        highest_similarity = 0.0

        for intent, examples in self.intent_database.items():
            for example in examples:
                example_vec = self.text_to_vector(example)
                sim = self.cosine_similarity(user_vec, example_vec)
                if sim > highest_similarity:
                    highest_similarity = sim
                    best_intent = intent

        # Strict scope enforcement
        if highest_similarity < self.similarity_threshold:
            return random.choice(self.gen_z_slang["scope_violation"])

        if best_intent in self.gen_z_slang:
            base_response = random.choice(self.gen_z_slang[best_intent])
        else:
            base_response = random.choice(self.gen_z_slang["general"])

        # Acknowledge slang if detected
        if detected_slang:
            slang_str = ", ".join(detected_slang)
            return f"(I see you dropping '{slang_str}' energy!) " + base_response

        return base_response
