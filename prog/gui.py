import tkinter as tk
from tkinter import scrolledtext

class SocialMediaChatApp:
    def __init__(self, root, nlp_engine):
        self.root = root
        self.nlp_engine = nlp_engine
        
        self.root.title("Social Media Project Chatbot (NLP + Gen Z)")
        self.root.geometry("520x620")
        self.root.config(bg="#1e1e1e")

        # Title Label
        title_label = tk.Label(
            root, text=" Social Media Project Assistant", 
            bg="#1e1e1e", fg="#00ffcc", font=("Helvetica", 14, "bold")
        )
        title_label.pack(pady=12)

        # Chat History Display Area
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, bg="#2d2d2d", fg="#ffffff", 
            font=("Helvetica", 11), state=tk.DISABLED, bd=0, highlightthickness=0
        )
        self.chat_display.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)
        
        # Tags for styling user vs bot texts
        self.chat_display.tag_config("user", foreground="#ff79c6", font=("Helvetica", 11, "bold"))
        self.chat_display.tag_config("bot", foreground="#8be9fd", font=("Helvetica", 11))

        # Bottom Frame for Input and Button
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
        """Safely injects text into the Tkinter ScrolledText widget."""
        self.chat_display.config(state=tk.NORMAL)
        if sender_type == "user":
            self.chat_display.insert(tk.END, f"\nYou: {message}\n", "user")
        else:
            self.chat_display.insert(tk.END, f"\n{message}\n", "bot")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        """Processes user input, triggers the NLP engine, and updates UI."""
        text = self.user_input.get().strip()
        if not text:
            return

        self.append_chat(text, "user")
        self.user_input.delete(0, tk.END)

        if text.lower() in ["exit", "quit"]:
            self.append_chat("Bot: Peace out! Catch you later.", "bot")
            self.root.after(1000, self.root.destroy)
            return

        # Fetch response via NLP engine instance
        response = self.nlp_engine.get_response(text)
        self.append_chat(response, "bot")