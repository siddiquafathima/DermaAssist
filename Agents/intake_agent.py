# intake_agent.py
import sys

ALLOWED_SKIN_TYPES = {"oily", "dry", "normal", "combination", "sensitive"}
ALLOWED_CONCERNS = {"acne", "pigmentation", "sensitivity", "aging", "dryness", "eczema", "rash"}

def _ask(prompt: str):
    """Basic input wrapper that handles 'quit' to exit."""
    val = input(prompt).strip()
    if val.lower() == "quit":
        print("Exiting — bye 👋")
        sys.exit(0)
    return val

def _ask_nonempty(prompt: str, allow_skip=False):
    while True:
        val = _ask(prompt)
        if allow_skip and val.lower() in {"", "skip", "none", "n/a"}:
            return None
        if val:
            return val
        print("⚠️ Please provide a value or type 'skip' to leave empty.")

def _ask_age(prompt: str, min_age=5, max_age=120):
    while True:
        val = _ask(prompt)
        if val.lower() in {"", "skip", "none", "n/a"}:
            return None
        try:
            age = int(val)
            if age < min_age or age > max_age:
                print(f"⚠️ Please enter an age between {min_age} and {max_age}.")
                continue
            return age
        except ValueError:
            print("⚠️ Age must be a number (e.g. 29). Type 'quit' to exit.")

def _ask_choice(prompt: str, choices:set):
    choices_list = ", ".join(sorted(choices))
    while True:
        val = _ask(prompt + f" ({choices_list})\n> ")
        if val.lower() in {"", "skip", "none", "n/a"}:
            return None
        v = val.lower().strip()
        if v in choices:
            return v
        print(f"⚠️ Invalid option. Please type one of: {choices_list}")

def interactive_intake():
    """
    Interactive intake flow with validation.
    Returns a dict with keys: name, age, skin_type, concern, user_id (None until set).
    """
    print("📋 Welcome to DermaAssist — Intake Agent")
    print("(type 'quit' at any prompt to exit)\n")

    name = _ask_nonempty("👤 Name (or type 'skip'):\n> ", allow_skip=True)
    age = _ask_age("🎂 Age (number, or type 'skip'):\n> ")
    skin_type = _ask_choice("✨ Skin type", ALLOWED_SKIN_TYPES)
    concern = _ask_choice("🔍 Main concern", ALLOWED_CONCERNS)

    profile = {
        "name": name or "",
        "age": age if age is not None else "",
        "skin_type": skin_type or "",
        "concern": concern or "",
        "user_id": None
    }

    return profile

if __name__ == "__main__":
    p = interactive_intake()
    print("\nCollected profile:")
    print(p)
