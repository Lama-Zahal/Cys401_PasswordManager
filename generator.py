import secrets
import string  # provides a ready collection of characters

SYMBOLS = "!@#$%^&*()-_=+"  # the special chars allowed


def generate_password(length=16, use_symbols=True) -> str:
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += SYMBOLS
    while True:
        pw = "".join(secrets.choice(chars) for _ in range(length))
        # keeps trying until it contains every character type:
        # one lowercase letter, one uppercase letter, one digit, and one symbol
        if (any(c.islower() for c in pw)
                and any(c.isupper() for c in pw)
                and any(c.isdigit() for c in pw)
                and (not use_symbols or any(c in SYMBOLS for c in pw))):
            return pw


def check_strength(password: str):
    # returns (label, tips)
    score, tips = 0, []  # starts with zero, then adds 1 for each rule that is met
    if len(password) >= 12:
        score += 1  # adding 1 to the score if the rule is met
    else:
        tips.append("Use at least 12 characters")
    if len(password) >= 16:
        score += 1
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    else:
        tips.append("Mix uppercase and lowercase letters")
    if any(c.isdigit() for c in password):
        score += 1
    else:
        tips.append("Add numbers")
    if any(c in SYMBOLS for c in password):
        score += 1
    else:
        tips.append("Add symbols")#provides the tip

    label = "Weak" if score <= 2 else "Medium" if score <= 4 else "Strong"
    return label, tips  # returns the label and the tips


def find_reused(entries):
    # finds passwords reused on more than one site
    seen, reused = set(), set()
    for e in entries:
        if e["password"] in seen:  # if it was already seen, add it to the reused set
            reused.add(e["password"])
        seen.add(e["password"])
    return reused