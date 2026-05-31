
import random
RESPONSES = {
    # --- Greetings ---
    "greeting": [
        "Hey there! Great to see you. I'm ARIA — what's on your mind?",
        "Hello! ARIA at your service. How can I help you today?",
        "Hi! Lovely to meet you. Ask me anything!",
    ],

    # --- Farewell / Exit (used for display before breaking the loop) ---
    "farewell": [
        "Goodbye! It was a pleasure chatting. Stay curious! ",
        "See you later! Come back anytime you have questions. ",
        "Bye! Take care and keep exploring. ",
    ],

    # --- How are you ---
    "wellbeing": [
        "Running smoothly, thanks for asking! All circuits nominal. ",
        "I'm doing great — no bugs today (that I know of)! How about you?",
        "Fantastic! Being an AI has its perks — I never have a bad day.",
    ],

    # --- What is AI ---
    "what_is_ai": [
        (
            "AI stands for Artificial Intelligence — the field of making machines "
            "think, learn, and solve problems. Funny enough, I'm a (very simple) example!"
        ),
        (
            "Artificial Intelligence is the science of building systems that can perform "
            "tasks that normally require human intelligence, like understanding language or "
            "recognising patterns."
        ),
    ],

    # --- What can you do / Help ---
    "help": [
        (
            "Here's what I understand:\n"
            "  • Greetings  : hello, hi, hey\n"
            "  • Wellbeing  : how are you\n"
            "  • About AI   : what is ai, tell me about ai\n"
            "  • Jokes      : tell me a joke, joke\n"
            "  • Time/Date  : what time is it, what's the date\n"
            "  • Fun fact   : fun fact, give me a fact\n"
            "  • About me   : who are you, what are you\n"
            "  • Exit       : bye, quit, exit\n"
            "Just type naturally and I'll do my best!"
        ),
    ],

    # --- Jokes ---
    "joke": [
        "Why do programmers prefer dark mode? Because light attracts bugs! ",
        "I told a joke about UDP once… I'm not sure if anyone got it.",
        "Why was the computer cold? Because it left its Windows open! ",
        "Algorithm: a word used by programmers when they don't want to explain what they did.",
    ],

    # --- Time / Date (static acknowledgement — no real-time clock needed) ---
    "time_date": [
        "I don't have access to a live clock, but your device's taskbar always knows! ",
        "Check the bottom-right corner of your screen — much more reliable than me for that! ",
    ],

    # --- Fun facts ---
    "fun_fact": [
        "Fun fact: The first computer bug was an actual bug — a moth found in a Harvard relay in 1947! ",
        "Fun fact: There are more possible chess games than atoms in the observable universe. ",
        "Fun fact: The average person blinks about 15–20 times per minute — but only 3–8 times while reading! ",
        "Fun fact: Honey never spoils. Archaeologists have found 3,000-year-old honey in Egyptian tombs — still edible! 🍯",
    ],

    # --- Who / What are you ---
    "identity": [
        (
            "I'm ARIA — Artificially Responsive Intelligent Assistant. "
            "I'm a rule-based chatbot built in Python. Simple, but proud of it! "
        ),
        "I'm ARIA, your friendly Python-powered chatbot. No neural networks, just good old dictionaries and logic!",
    ],

    # --- Fallback for unrecognised input ---
    "unknown": [
        "Hmm, I'm not sure I understand that. Type 'help' to see what I can do!",
        "I don't quite follow. Could you rephrase? (Tip: type 'help' for a list of topics.)",
        "That's a bit beyond my current knowledge. Try 'help' to see my capabilities!",
    ],
}


INTENT_MAP = {
    # Greetings
    "hello":               "greeting",
    "hi":                  "greeting",
    "hey":                 "greeting",
    "howdy":               "greeting",
    "greetings":           "greeting",
    "sup":                 "greeting",
    "yo":                  "greeting",

    # Farewell / exit triggers (loop logic handles the break)
    "bye":                 "farewell",
    "goodbye":             "farewell",
    "exit":                "farewell",
    "quit":                "farewell",
    "see you":             "farewell",
    "later":               "farewell",

    # Wellbeing
    "how are you":         "wellbeing",
    "how are you doing":   "wellbeing",
    "how's it going":      "wellbeing",
    "are you okay":        "wellbeing",

    # What is AI
    "what is ai":          "what_is_ai",
    "what's ai":           "what_is_ai",
    "tell me about ai":    "what_is_ai",
    "explain ai":          "what_is_ai",
    "artificial intelligence": "what_is_ai",

    # Help
    "help":                "help",
    "what can you do":     "help",
    "commands":            "help",
    "options":             "help",
    "menu":                "help",

    # Jokes
    "tell me a joke":      "joke",
    "joke":                "joke",
    "make me laugh":       "joke",
    "funny":               "joke",

    # Time / Date
    "what time is it":     "time_date",
    "what's the time":     "time_date",
    "what time":           "time_date",
    "what's the date":     "time_date",
    "what date":           "time_date",
    "today's date":        "time_date",

    # Fun facts
    "fun fact":            "fun_fact",
    "give me a fact":      "fun_fact",
    "tell me a fact":      "fun_fact",
    "random fact":         "fun_fact",

    # Identity
    "who are you":         "identity",
    "what are you":        "identity",
    "your name":           "identity",
    "what's your name":    "identity",
    "tell me about yourself": "identity",
}

# Exit intents that should break the conversation loop
EXIT_INTENTS = {"farewell"}



def sanitize(text: str) -> str:
    """Lowercase and strip leading/trailing whitespace from user input."""
    return text.lower().strip()


def get_intent(user_input: str) -> str:
    """
    Resolve user input to an intent name using the INTENT_MAP.

    Strategy:
    1. Exact match in INTENT_MAP           → fastest path, O(1)
    2. Substring scan of multi-word keys   → handles partial phrases
    3. Fallback to "unknown"               → always returns a valid intent
    """
    # 1. Exact match
    if user_input in INTENT_MAP:
        return INTENT_MAP[user_input]
    # 2. Substring scan (for multi-word keys)
    sorted_keys = sorted(INTENT_MAP.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in user_input:
            return INTENT_MAP[key]

    # 3. Default fallback
    return "unknown"


def get_response(intent: str) -> str:
    """
    Retrieve a (randomly selected) response for the given intent.
    Uses dict.get() with a fallback list so it never raises a KeyError.
    """
    options = RESPONSES.get(intent, RESPONSES["unknown"])
    return random.choice(options)


def main():
    bot_name = "ARIA"

    print(f"\nWelcome! I'm {bot_name} (Artificially Responsive Intelligent Assistant).")
    print("Type 'help' to see what I can do, or 'bye' to exit.\n")

    while True:  # Infinite loop — exits only on a farewell intent
        # --- Get and sanitize user input ---
        raw_input = input("You: ")
        clean_input = sanitize(raw_input)

        # Guard against empty input
        if not clean_input:
            print(f"{bot_name}: It looks like you didn't type anything. Need help? Try 'help'.\n")
            continue

        # --- Resolve intent ---
        intent = get_intent(clean_input)

        # --- Nested condition: context-aware handling for exit intents ---
        if intent in EXIT_INTENTS:
            farewell_msg = get_response("farewell")
            print(f"{bot_name}: {farewell_msg}\n")
            break  # Clean exit from the loop

        # --- Nested condition: encourage help for very short unknowns ---
        if intent == "unknown" and len(clean_input) <= 3:
            print(f"{bot_name}: Not sure what '{raw_input}' means. Try typing 'help' to see my topics!\n")
            continue

        # --- Standard response ---
        response = get_response(intent)
        print(f"{bot_name}: {response}\n")


if __name__ == "__main__":
    main()
