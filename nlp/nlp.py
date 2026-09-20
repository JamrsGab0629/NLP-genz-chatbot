import csv
import os
import random
import re
import tkinter as tk
from tkinter import scrolledtext


class GenZChatbotApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Gen Z Slang Chatbot (No Cap Edition)")
    self.root.geometry("500x600")
    self.root.config(bg="#1e1e1e")

    # 1. Load the local dataset on startup
    self.slang_db = self.load_local_dataset("all_slangs.csv")

    # 2. Build the GUI Layout
    self.create_widgets()

  def load_local_dataset(self, filename):
    """Loads the dataset dynamically next to the script using standard libraries."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    slang_database = {}
    try:
      with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
          term = row.get("Slang", "").strip().lower()
          if term:
            slang_database[term] = {
                "description": row.get("Description", "").strip(),
                "example": row.get("Example", "").strip(),
            }
      print(f"Successfully loaded {len(slang_database)} terms locally!")
      return slang_database
    except FileNotFoundError:
      print(f"Error: Could not find '{filename}' at {file_path}.")
      return {}

  def get_response(self, user_input):
    """Scans the entire dataset dynamically:

    1. Checks for exact slang matches with randomized response templates.
    2. If no exact slang is found, scans all descriptions/examples for keyword
    overlap.
    3. Falls back to dynamic Gen Z responses if nothing matches.
    """
    user_input_lower = user_input.lower()
    user_words = set(re.findall(r"\w+", user_input_lower))

    # --- STEP 1: Direct Slang Match (with randomized response styles) ---
    for slang, info in self.slang_db.items():
      pattern = r"\b" + re.escape(slang) + r"\b"
      if re.search(pattern, user_input_lower):
        desc = info["description"]
        ex = info["example"]

        # Randomize how the bot answers so it never feels repetitive!
        templates = [
            f"No cap, '{slang.upper()}' means: {desc}\nExample: \"{ex}\"",
            f"Oh, you're talking about {slang.upper()}? That's when: {desc}\nPeep this example: \"{ex}\"",
            f"Bet. {slang.upper()} is defined as: {desc}\nLike when you say: \"{ex}\"",
        ]
        return random.choice(templates)

    # --- STEP 2: Deep Dataset Scan (Keyword Overlap) ---
    best_match = None
    max_matches = 0

    for slang, info in self.slang_db.items():
      row_text = f"{slang} {info['description']} {info['example']}".lower()
      row_words = set(re.findall(r"\w+", row_text))

      filler_words = {
          "is",
          "the",
          "a",
          "to",
          "it",
          "i",
          "you",
          "what",
          "mean",
          "and",
          "of",
          "in",
      }
      common_words = user_words.intersection(row_words) - filler_words

      if len(common_words) > max_matches and len(common_words) >= 2:
        max_matches = len(common_words)
        best_match = (slang, info)

    if best_match:
      slang, info = best_match
      return (
          f"Lowkey sounds like you're talking about '{slang.upper()}' based on"
          f" your message.\nDefinition: {info['description']}\nExample:"
          f' "{info["example"]}"'
      )

    # --- STEP 3: Dynamic Gen Z Fallback ---
    fallbacks = [
        (
            "That's kind of mid... I scanned all 1,571 terms in my database and"
            " couldn't quite catch that vibe."
        ),
        (
            "No cap, I'm drawing a blank on that one. Try asking about a"
            " different term or phrase!"
        ),
        (
            "That's sus... my local dataset doesn't have a match for that. Try"
            " another word!"
        ),
    ]
    return random.choice(fallbacks)

  def create_widgets(self):
    # Chat History Display Area
    self.chat_display = scrolledtext.ScrolledText(
        self.root, wrap=tk.WORD, state=tk.DISABLED, bg="#2d2d2d", fg="#ffffff"
    )
    self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    self.chat_display.config(font=("Arial", 11))

    # Configure tags for styling user vs bot text
    self.chat_display.tag_config("user", foreground="#4da6ff")
    self.chat_display.tag_config("bot", foreground="#00ffcc")

    # Input Frame (Text entry + Send button)
    input_frame = tk.Frame(self.root, bg="#1e1e1e")
    input_frame.pack(padx=10, pady=10, fill=tk.X)

    self.user_entry = tk.Entry(
        input_frame,
        font=("Arial", 12),
        bg="#333333",
        fg="#ffffff",
        insertbackground="white",
    )
    self.user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
    self.user_entry.bind("<Return>", self.send_message)  # Press Enter to send

    send_button = tk.Button(
        input_frame,
        text="Send",
        command=self.send_message,
        bg="#00ffcc",
        fg="#000000",
        font=("Arial", 10, "bold"),
    )
    send_button.pack(side=tk.RIGHT)

    # Initial Bot Greeting
    self.append_chat(
        "Chatbot: Yo! Dataset loaded with "
        f"{len(self.slang_db)} terms. What slang are we looking up today?"
        "\n\n",
        "bot",
    )

  def send_message(self, event=None):
    user_text = self.user_entry.get().strip()
    if not user_text:
      return

    # Display User Message
    self.append_chat(f"You: {user_text}\n", "user")
    self.user_entry.delete(0, tk.END)

    # Handle exit command
    if user_text.lower() == "exit":
      self.append_chat("Chatbot: Bet, catch you later! Slay the day.\n", "bot")
      self.root.after(1500, self.root.destroy)
      return

    # Get Bot Response and Display
    response = self.get_response(user_text)
    self.append_chat(f"Chatbot: {response}\n\n", "bot")

  def append_chat(self, text, tag):
    self.chat_display.config(state=tk.NORMAL)
    self.chat_display.insert(tk.END, text, tag)
    self.chat_display.config(state=tk.DISABLED)
    self.chat_display.see(tk.END)


if __name__ == "__main__":
  root = tk.Tk()
  app = GenZChatbotApp(root)
  root.mainloop()