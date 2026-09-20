"""
GenZ Slang Bot
==============
A simple desktop chatbot, built with Tkinter only (Python standard library —
no external/pip packages). It reads a CSV database of Gen Z / internet slang,
scans whatever the user types for any slang it recognises, and explains it
back in a randomly-varied ("versatile") way so it doesn't sound robotic.

Approach: database + keyword detection (regex, longest-match-first, with a
case-sensitivity rule so common English words that also happen to be listed
as ALL-CAPS internet acronyms — e.g. "WAS", "SO", "AT" — don't get flagged
on every ordinary sentence; you can still trigger those by SHOUTING them).

Files needed side by side:
    genz_slang_bot.py   <- this file
    all_slangs.csv       <- the slang database (Slang, Description, Example, Context)

Run with:  python genz_slang_bot.py
"""

import os
import re
import csv
import random
import tkinter as tk
from tkinter import font as tkfont

# ---------------------------------------------------------------------------
# 1. Load the slang database
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "all_slangs.csv")


def load_slang_database(path):
    """Read the CSV into {lowercase_term: [ {raw, description, example, context}, ... ]}.
    A list is used per term because the dataset sometimes has more than one
    definition for the same word (e.g. slang evolves / has multiple senses)."""
    db = {}
    if not os.path.exists(path):
        return db
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            raw = (row.get("Slang") or "").strip()
            if not raw:
                continue
            key = raw.lower()
            db.setdefault(key, []).append(
                {
                    "raw": raw,
                    "description": (row.get("Description") or "").strip(),
                    "example": (row.get("Example") or "").strip(),
                    "context": (row.get("Context") or "").strip(),
                }
            )
    return db


SLANG_DB = load_slang_database(CSV_PATH)

# Match longest terms first so multi-word slang ("this ain't it, chief") wins
# over a shorter term hiding inside it, and so overlapping single words don't
# get double-matched.
_TERMS_BY_LENGTH = sorted(SLANG_DB.keys(), key=len, reverse=True)
_SLANG_PATTERN = (
    re.compile(
        r"(?<!\w)(" + "|".join(re.escape(t) for t in _TERMS_BY_LENGTH) + r")(?!\w)",
        re.IGNORECASE,
    )
    if _TERMS_BY_LENGTH
    else None
)


def _resolve_entries(key, matched_text):
    """Decide which definition(s) apply to a regex match.

    Some entries in the dataset are genuine ALL-CAPS internet acronyms that
    happen to collide with ordinary English words when lowercased (e.g. the
    acronym "WAS" vs. the everyday word "was"). To keep the bot usable in
    normal conversation, an acronym that is stored in ALL CAPS only counts as
    a hit if the user *also* typed it in ALL CAPS. Everyday slang (stored in
    lower/Title case) matches regardless of how it's typed.
    """
    entries = SLANG_DB.get(key, [])
    upper_only = [e for e in entries if e["raw"].isupper()]
    everyday = [e for e in entries if not e["raw"].isupper()]
    if matched_text.isupper() and upper_only:
        return upper_only
    if everyday:
        return everyday
    return None


def find_slang(text):
    """Return [(matched_text, entry_dict), ...] for every slang term found,
    in the order it appears in the text."""
    if not _SLANG_PATTERN:
        return []
    hits = []
    for m in _SLANG_PATTERN.finditer(text):
        matched_text = m.group(1)
        entries = _resolve_entries(matched_text.lower(), matched_text)
        if entries:
            hits.append((matched_text, random.choice(entries)))
    return hits


# ---------------------------------------------------------------------------
# 2. Versatile response generation
#    (multiple phrasings picked at random, and near-repeats are avoided so
#    the bot doesn't give the exact same line twice in a row)
# ---------------------------------------------------------------------------
_last_pick = {}


def pick(category, options):
    """random.choice, but avoids repeating the same option twice in a row
    for a given category, so replies feel more natural/varied over time."""
    if not options:
        return ""
    previous = _last_pick.get(category)
    pool = [o for o in options if o != previous] or options
    choice = random.choice(pool)
    _last_pick[category] = choice
    return choice


def lower_first(s):
    return s[0].lower() + s[1:] if s else s


SINGLE_SLANG_TEMPLATES = [
    'Oh, "{term}"? That means {desc}. Example: {example}',
    '"{term}" = {desc}. Kinda like: "{example}"',
    'Ha, caught that — "{term}" basically means {desc}.',
    'You said "{term}"! That\'s slang for {desc}.',
    'Fun fact: "{term}" is used to mean {desc}. {context}',
    'No cap, "{term}" means {desc}. 💯',
    '"{term}"? Easy — {desc}. Someone might say: "{example}"',
]

MULTI_SLANG_INTROS = [
    "Okay you're speaking fluent Gen Z rn, let me break it down:",
    "Whoa, {n} slang terms in one message?! Here's the tea:",
    "Say less, I gotchu — here's what you dropped:",
    "Bet, let's translate that real quick:",
    "Sheesh, a whole vocabulary lesson. Here goes:",
]

MULTI_SLANG_LINE = '• "{term}" — {desc}'


def build_slang_reply(hits):
    if len(hits) == 1:
        term, entry = hits[0]
        template = pick("single_" + term.lower(), SINGLE_SLANG_TEMPLATES)
        example = entry["example"] or "...(no example on file, but you get the idea)"
        context = entry["context"]
        return template.format(
            term=term,
            desc=lower_first(entry["description"]),
            example=example,
            context=context,
        )

    intro = pick("multi_intro", MULTI_SLANG_INTROS).format(n=len(hits))
    lines = [intro]
    seen = set()
    for term, entry in hits:
        if term.lower() in seen:
            continue
        seen.add(term.lower())
        lines.append(MULTI_SLANG_LINE.format(term=term, desc=lower_first(entry["description"])))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. General small-talk (pattern-based), for when no slang is detected
# ---------------------------------------------------------------------------
GENERAL_PATTERNS = [
    ("greeting", re.compile(r"\b(hi|hello|hey+|yo+|sup|wassup|what'?s up|howdy)\b", re.I), [
        "Heyyy 👋 what's good?",
        "Yo! Hit me with some slang and I'll decode it for you.",
        "Hiii, ready to talk Gen Z whenever you are.",
        "Sup! Try me with some slang, I dare you 😏",
    ]),
    ("how_are_you", re.compile(r"how\s*(are|r)\s*(you|u|ya)\b", re.I), [
        "I'm vibing, thanks for asking! How about you?",
        "Living my best digital life, no cap. You good?",
        "Can't complain — I just sit here decoding slang all day.",
    ]),
    ("thanks", re.compile(r"\b(thanks|thank you|ty|thx)\b", re.I), [
        "Anytime, that's what I'm here for!",
        "No worries, periodt.",
        "You're welcome, fam.",
    ]),
    ("bye", re.compile(r"\b(bye|goodbye|see\s?ya|see you|later|peace out|gtg|cya)\b", re.I), [
        "Peace out ✌️",
        "Later! Come back with more slang to decode.",
        "Bye bye, stay iconic.",
    ]),
    ("identity", re.compile(r"(your name|who are you|what are you)", re.I), [
        "I'm the GenZ Slang Bot — here to decode the internet for you.",
        "Just a bot who lives and breathes Gen Z slang, no cap.",
    ]),
    ("help", re.compile(r"\b(help|what can you do|commands?)\b", re.I), [
        "Type any sentence and I'll spot the Gen Z slang in it and explain it. "
        "Say 'random slang' for a surprise word!",
        "I scan whatever you type for slang and translate it. Try 'random slang' "
        "if you want me to teach you a new one.",
    ]),
]

RANDOM_SLANG_TRIGGER = re.compile(
    r"\b(random slang|surprise me|teach me( a (word|slang))?|random word|"
    r"give me a (word|slang)|new (word|slang))\b",
    re.I,
)

FALLBACK_RESPONSES = [
    "Hmm, didn't catch any slang in that one — try me with something like \"that's bussin\" or \"no cap\".",
    "I got nothing on that, chief. Throw some slang my way!",
    "Not sure what to say to that, but I'm all ears for some Gen Z slang.",
    "That went a little over my head — got any slang for me to translate?",
    "I'm just a slang bot, so I'm best with sentences that have some slang in 'em!",
]

EMPTY_RESPONSES = [
    "Say something, I don't bite!",
    "...you gonna type something or what? 👀",
]


def random_slang_fact():
    if not SLANG_DB:
        return "My slang dictionary didn't load, so I've got nothing to teach you right now 😅"
    key = random.choice(list(SLANG_DB.keys()))
    entry = random.choice(SLANG_DB[key])
    example = entry["example"] or "...(no example on file)"
    return f'Here\'s a random one: "{entry["raw"]}" — {lower_first(entry["description"])}. e.g. "{example}"'


def get_bot_response(user_text):
    text = user_text.strip()
    if not text:
        return pick("empty", EMPTY_RESPONSES)

    if RANDOM_SLANG_TRIGGER.search(text):
        return random_slang_fact()

    hits = find_slang(text)
    if hits:
        return build_slang_reply(hits)

    for category, pattern, responses in GENERAL_PATTERNS:
        if pattern.search(text):
            return pick(category, responses)

    return pick("fallback", FALLBACK_RESPONSES)


# ---------------------------------------------------------------------------
# 4. Tkinter GUI
# ---------------------------------------------------------------------------
class ChatApp:
    OUTER_BG = "#2c2c34"
    CARD_BG = "#f5f5f7"
    HEADER_BG = "#ffffff"
    ACCENT = "#3B82F6"
    BOT_BUBBLE = "#FFC94A"
    USER_BUBBLE = "#3B82F6"
    BOT_TEXT = "#20232a"
    USER_TEXT = "#ffffff"

    def __init__(self, root):
        self.root = root
        root.title("GenZ Slang Bot")
        root.geometry("480x680")
        root.minsize(360, 480)
        root.configure(bg=self.OUTER_BG)

        card = tk.Frame(root, bg=self.CARD_BG)
        card.pack(fill="both", expand=True, padx=14, pady=14)

        self._build_header(card)
        self._build_chat_area(card)
        self._build_input_area(card)

        term_count = len(SLANG_DB)
        intro = (
            f"Heyyy! I'm your GenZ Slang Bot 🗨️ — drop any sentence and I'll spot "
            f"the slang in it (I know {term_count} terms). Type \"random slang\" "
            f"for a surprise, or just say hi!"
        ) if term_count else (
            "Heyyy! I'm your GenZ Slang Bot 🗨️ — heads up, I couldn't find "
            "all_slangs.csv next to me, so slang detection is off, but we can "
            "still chat!"
        )
        self._add_bot_message(intro)

    # -- header -------------------------------------------------------
    def _build_header(self, parent):
        header = tk.Frame(parent, bg=self.HEADER_BG)
        header.pack(fill="x")

        tk.Frame(header, bg=self.ACCENT, height=4, width=60).pack(
            anchor="w", pady=(14, 8), padx=18
        )
        title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
        tk.Label(
            header, text="GenZ Slang Bot", font=title_font, bg=self.HEADER_BG, fg="#111111"
        ).pack(anchor="w", padx=18)
        tk.Label(
            header,
            text="no cap, I speak fluent internet",
            font=("Helvetica", 10),
            bg=self.HEADER_BG,
            fg="#777777",
        ).pack(anchor="w", padx=18, pady=(0, 14))

    # -- scrollable chat log -------------------------------------------
    def _build_chat_area(self, parent):
        container = tk.Frame(parent, bg=self.CARD_BG)
        container.pack(fill="both", expand=True, padx=8, pady=(6, 8))

        self.canvas = tk.Canvas(container, bg=self.CARD_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.msg_frame = tk.Frame(self.canvas, bg=self.CARD_BG)

        self.msg_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.msg_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_canvas_resize)
        # mouse-wheel support (Windows/macOS use <MouseWheel>, Linux uses Button-4/5)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # -- input bar ------------------------------------------------------
    def _build_input_area(self, parent):
        bar = tk.Frame(parent, bg=self.HEADER_BG)
        bar.pack(fill="x", side="bottom")
        inner = tk.Frame(bar, bg=self.HEADER_BG)
        inner.pack(fill="x", padx=14, pady=14)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            inner,
            textvariable=self.entry_var,
            font=("Helvetica", 12),
            relief="flat",
            bg="#eeeeee",
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self._on_send())
        self.entry.focus_set()

        send_btn = tk.Button(
            inner,
            text="Send",
            command=self._on_send,
            bg=self.ACCENT,
            fg="white",
            relief="flat",
            font=("Helvetica", 11, "bold"),
            padx=16,
            pady=6,
            activebackground="#2563eb",
            activeforeground="white",
            cursor="hand2",
        )
        send_btn.pack(side="right")

    # -- message handling -------------------------------------------------
    def _on_send(self):
        text = self.entry_var.get().strip()
        if not text:
            return
        self.entry_var.set("")
        self._add_user_message(text)
        # tiny delay so the bot reply doesn't feel instant/robotic
        self.root.after(300, lambda: self._add_bot_message(get_bot_response(text)))

    def _add_user_message(self, text):
        self._add_bubble(text, side="right", bg=self.USER_BUBBLE, fg=self.USER_TEXT)

    def _add_bot_message(self, text):
        self._add_bubble(text, side="left", bg=self.BOT_BUBBLE, fg=self.BOT_TEXT)

    def _add_bubble(self, text, side, bg, fg):
        row = tk.Frame(self.msg_frame, bg=self.CARD_BG)
        row.pack(fill="x", pady=4, padx=6)

        bubble = tk.Label(
            row,
            text=text,
            bg=bg,
            fg=fg,
            justify="left",
            anchor="w",
            wraplength=300,
            padx=12,
            pady=8,
            font=("Helvetica", 11),
        )
        bubble.pack(side="right" if side == "right" else "left", anchor="e" if side == "right" else "w")

        self.msg_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1.0)


def main():
    root = tk.Tk()
    ChatApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
