import tkinter as tk
from nlp_engine import NLPEngine
from gui import SocialMediaChatApp

def main():
    root = tk.Tk()
    
    # Initialize dependencies separately (Dependency Injection pattern)
    nlp_engine = NLPEngine(similarity_threshold=0.12)
    app = SocialMediaChatApp(root, nlp_engine)
    
    root.mainloop()

if __name__ == "__main__":
    main()