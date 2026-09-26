import re

class TextPreprocessor:
   
    
    def normalize(self, text: str) -> str:
      
        if not text:
            return ""
            
        text = text.lower()
        
        
        text = re.sub(r'(.)\1{2,}', r'\1\1', text)
        
        
        text = re.sub(r'\bgonna\b', 'going to', text)
        text = re.sub(r'\bwanna\b', 'want to', text)
        text = re.sub(r'\bgotta\b', 'got to', text)

        
        return text