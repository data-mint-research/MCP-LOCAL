from datetime import datetime

DIALOG_STATE = {
    "turn_id": 0,
    "history": []
}

def handle_input(user_input):
    DIALOG_STATE["turn_id"] += 1
    response = generate_response(user_input)

    DIALOG_STATE["history"].append({
        "turn": DIALOG_STATE["turn_id"],
        "timestamp": datetime.utcnow().isoformat(),
        "user_input": user_input,
        "response": response
    })

    return response

def generate_response(user_input):
    if not user_input or user_input.strip() == "":
        return "Ich habe dich nicht verstanden."
    if "ziel" in user_input.lower():
        return "Was möchtest du mit deinem Ziel erreichen?"
    return f"Echo: {user_input}"