import math
import re
from collections import Counter
import random
from constants import INTENT_DATABASE, GEN_Z_SLANG, GEN_Z_KEYWORDS

# Common stop words to ignore so they don't cause false positive matches
STOP_WORDS = {"what", "is", "the", "of", "a", "an", "to", "how", "do", "we", "i", "can", "you", "help", "me", "are"}

class NLPEngine:
    def __init__(self, similarity_threshold=0.25):  # Raised threshold for stricter scope
        self.intent_database = INTENT_DATABASE
        self.gen_z_slang = GEN_Z_SLANG
        self.gen_z_keywords = GEN_Z_KEYWORDS
        self.similarity_threshold = similarity_threshold

    def tokenize(self, text):
        """Extracts alphanumeric tokens, lowercases them, and removes stop words."""
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter out stop words to keep only meaningful keywords for NLP matching
        filtered_words = [w for w in words if w not in STOP_WORDS]
        return filtered_words

    def text_to_vector(self, text):
        """Converts filtered tokens into a frequency Counter vector."""
        words = self.tokenize(text)
        return Counter(words)

    def cosine_similarity(self, vec1, vec2):
        """Computes cosine similarity between two word vectors."""
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        return float(numerator) / denominator

    def detect_user_slang(self, text):
        """Scans user input to find exact Gen Z slang matches without double-matching substrings."""
        text_lower = text.lower()
        found_slang = []
        
        multi_word_slang = [s for s in self.gen_z_keywords if " " in s]
        single_word_slang = [s for s in self.gen_z_keywords if " " not in s]
        
        for slang in multi_word_slang:
            if slang in text_lower:
                found_slang.append(slang)
                text_lower = text_lower.replace(slang, "")
        
        # Tokenize using standard regex here (don't filter stop words for slang detection)
        tokens = re.findall(r'\b\w+\b', text_lower)
        for slang in single_word_slang:
            if slang in tokens:
                found_slang.append(slang)
                    
        return found_slang

    def get_response(self, user_input):
        """Evaluates user input via NLP, detects user slang, and enforces strict scope."""
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

        # Strict scope enforcement (Now blocks out-of-scope questions reliably)
        if highest_similarity < self.similarity_threshold:
            return random.choice(self.gen_z_slang["scope_violation"])

        if best_intent in self.gen_z_slang:
            base_response = random.choice(self.gen_z_slang[best_intent])
        else:
            base_response = random.choice(self.gen_z_slang["general"])

        # Acknowledge slang if detected
        if detected_slang:
            slang_str = ", ".join(detected_slang)
            acknowledgment = f"(I see you dropping '{slang_str}' energy!) "
            return acknowledgment + base_response

        return base_response