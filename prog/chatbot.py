import math
import re
from collections import Counter
import random
import tkinter as tk
from tkinter import scrolledtext, ttk

# NLP Intent Database (Mapping example sentences to project categories)
INTENT_DATABASE = {
    "algorithm": [
        "how does the feed algorithm work",
        "we need to fix the recommendation algorithm for the app",
        "pushing viral content on the feed algorithm"
    ],
    "feature": [
        "what new features should we add to the social media app",
        "building the direct messaging and story feature",
        "adding a live streaming feature for creators"
    ],
    "design": [
        "the user interface ui design looks a bit mid",
        "we need a cleaner dark mode aesthetic for the app design",
        "improving the mobile app ux and layout"
    ],
    "post": [
        "how users create and publish video posts",
        "should we allow long text posts or just reels",
        "engagement rates on image and video posts"
    ],
    "profile": [
        "customizing user profile pages and bios",
        "showing follower counts and stats on profiles"
    ]
}

# Gen Z Slang Response Library
GEN_Z_SLANG = {
    "algorithm": [
        "No cap, our feed algorithm needs to push more viral short-form content.",
        "Bet, the algorithm is cooking right now. Users are gonna love the FYP!"
    ],
    "feature": [
        "That feature is straight fire, no cap! Let's prioritize building it.",
        "Adding that would defs be a major W for the app."
    ],
    "design": [
        "The UI design is looking a bit mid right now, we gotta make it slay.",
        "Bet, let's keep the dark mode aesthetic clean and modern, no cap."
    ],
    "post": [
        "Posting videos and reels is going to get us insane engagement.",
        "Cap or no cap, do you think text posts will actually take off on our app?"
    ],
    "profile": [
        "User profiles definitely need a custom bio section and follower stats, obviously.",
        "That profile layout is giving clean aesthetics, total slay."
    ],
    "general": [
        "No cap, that social media project idea sounds solid. Tell me more about it!",
        "That's a major W for the roadmap. What else are we adding?"
    ],
    "scope_violation": [
        "That sounds kind of sus... let's stick to talking about our social media project, bet?",
        "No cap, I only want to talk about the social media app right now. What's the next feature?"
    ]
}

def tokenize(text):
    """NLP Tokenizer: Lowercases text and extracts alphanumeric tokens."""
    return re.findall(r'\b\w+\b', text.lower())

def text_to_vector(text):
    """Converts text tokens into a Bag-of-Words frequency vector."""
    words = tokenize(text)
    return Counter(words)

def cosine_similarity(vec1, vec2):
    """Calculates Cosine Similarity between two text vectors (Pure Python NLP)."""
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator

def get_nlp_response(user_input):
    """Processes user input using NLP similarity scoring and returns a Gen Z response."""
    user_vec = text_to_vector(user_input)
    
    if not user_vec:
        return random.choice(GEN_Z_SLANG["scope_violation"])

    best_intent = None
    highest_similarity = 0.0
    similarity_threshold = 0.12  # Strict scope guardrail

    # Compare input against intent database
    for intent, examples in INTENT_DATABASE.items():
        for example in examples:
            example_vec = text_to_vector(example)
            sim = cosine_similarity(user_vec, example_vec)
            if sim > highest_similarity:
                highest_similarity = sim
                best_intent = intent

    # Enforce scope: If similarity is below threshold, redirect the user
    if highest_similarity < similarity_threshold:
        return random.choice(GEN_Z_SLANG["scope_violation"])

    if best_intent in GEN_Z_SLANG:
        return random.choice(GEN_Z_SLANG[best_intent])
        
    return random.choice(GEN_Z_SLANG["general"])


class SocialMediaChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Media Project Chatbot (NLP + Gen Z)")
        self.root.geometry("520x620")
        self.root.config(bg="#1e1e1e")

        # Title Label
        title_label = tk.Label(
            root, text="🚀 Social Media Project Assistant", 
            bg="#1e1e1e", fg="#00ffcc", font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=12)

        # Chat History Display Area (Fixed wrap=tk.WORD)
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, bg="#2d2d2d", fg="#ffffff", 
            font=("Helvetica", 11), state=tk.DISABLED, bd=0, highlightthickness=0
        )
        self.chat_display.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        
        # Configure custom font tags for messages
        self.chat_display.tag_config("user", foreground="#ff79c6", font=("Helvetica", 11, "bold"))
        self.chat_display.tag_config("bot", foreground="#8be9fd", font=("Helvetica", 11))

        # Bottom Frame for User Input and Send Button
        bottom_frame = tk.Frame(root, bg="#1e1e1e")
        bottom_frame.pack(padx=15, pady=15, fill=tk.X)

        # Input Text Box
        self.user_input = tk.Entry(
            bottom_frame, bg="#333333", fg="#ffffff", insertbackground="white",
            font=("Helvetica", 12), bd=0
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.user_input.bind("<Return>", self.send_message)

        # Send Button
        send_btn = tk.Button(
            bottom_frame, text="Send", bg="#6272a4", fg="#ffffff",
            font=("Helvetica", 11, "bold"), bd=0, padx=15, command=self.send_message
        )
        send_btn.pack(side=tk.RIGHT, ipady=4)

        # Initial Welcome Message
        self.append_chat("Bot: Yo! Welcome to the Social Media Project app. No cap, let's talk app development.", "bot")

    def append_chat(self, message, sender_type):
        """Appends formatted messages to the text widget safely."""
        self.chat_display.config(state=tk.NORMAL)
        if sender_type == "user":
            self.chat_display.insert(tk.END, f"\nYou: {message}\n", "user")
        else:
            self.chat_display.insert(tk.END, f"\n{message}\n", "bot")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        """Handles user submission, processes via NLP, and updates GUI."""
        text = self.user_input.get().strip()
        if not text:
            return

        self.append_chat(text, "user")
        self.user_input.delete(0, tk.END)

        if text.lower() in ["exit", "quit"]:
            self.append_chat("Bot: Peace out! Catch you later.", "bot")
            self.root.after(1000, self.root.destroy)
            return

        # NLP Response Evaluation
        response = get_nlp_response(text)
        self.append_chat(response, "bot")

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialMediaChatApp(root)
    root.mainloop()