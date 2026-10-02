from preprocessor import TextPreprocessor
from constants import STOP_WORDS, INTENT_DATABASE
import re
from collections import Counter
import math

STOP_WORDS = {"what", "is", "the", "of", "a", "an", "to", "how", "do", "we", "i", "can", "you", "help", "me", "are"}



class NLPEngine:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.stop_words = STOP_WORDS

    def tokenize(self, text):
        """Normalizes text using preprocessor, extracts tokens, and removes stop words."""
        # Step 1: Let the preprocessor handle regex text normalization
        clean_text = self.preprocessor.normalize(text)
        
        # Step 2: Extract alphanumeric words
        words = re.findall(r'\b\w+\b', clean_text)
        
        # Step 3: Filter out stop words
        filtered_words = [w for w in words if w not in self.stop_words]
        
        return filtered_words
    
    
    def text_to_vector(self, text):
      
        words = self.tokenize(text)
        return Counter(words)

    def cosine_similarity(self, vec1, vec2):
      
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        return float(numerator) / denominator

    def detect_user_slang(self, text):
       
        text_lower = text.lower()
        found_slang = []
        
        multi_word_slang = [s for s in self.gen_z_keywords if " " in s]
        single_word_slang = [s for s in self.gen_z_keywords if " " not in s]
        
        for slang in multi_word_slang:
            if slang in text_lower:
                found_slang.append(slang)
                text_lower = text_lower.replace(slang, "")
        
        tokens = re.findall(r'\b\w+\b', text_lower)
        for slang in single_word_slang:
            if slang in tokens:
                found_slang.append(slang)
                    
        return found_slang

    def get_response(self, user_input):
      
        
     
        if "dumbel" in user_input.lower():
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
            acknowledgment = f"(I see you dropping '{slang_str}' energy!) "
            return acknowledgment + base_response

        return base_response