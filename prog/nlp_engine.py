import math
import re
from collections import Counter
import random
from constants import INTENT_DATABASE, GEN_Z_SLANG

class NLPEngine:
    def __init__(self, similarity_threshold=0.12):
        self.intent_database = INTENT_DATABASE
        self.gen_z_slang = GEN_Z_SLANG
        self.similarity_threshold = similarity_threshold

    def tokenize(self, text):
        """Extracts alphanumeric tokens and converts them to lowercase."""
        return re.findall(r'\b\w+\b', text.lower())

    def text_to_vector(self, text):
        """Converts tokens into a frequency Counter vector."""
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

    def get_response(self, user_input):
        """Evaluates user input via NLP and returns an appropriate response."""
        user_vec = self.text_to_vector(user_input)
        
        if not user_vec:
            return random.choice(self.gen_z_slang["scope_violation"])

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
            return random.choice(self.gen_z_slang[best_intent])
            
        return random.choice(self.gen_z_slang["general"])