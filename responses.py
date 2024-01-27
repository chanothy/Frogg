from random import choice, randint

def get_response(user_input: str):
    lowered = user_input.lower()

    if lowered == " ":
        return "Speak you fool."
    elif "hello" in lowered:
        return "Greetings! (Winton)"

