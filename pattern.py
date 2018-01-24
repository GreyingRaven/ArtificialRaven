"""
Ban patterns:
add patterns that mean an inmediate ban.
NOT the same as timeout patterns.
"""
BAN_PAT = [
    r"swear",
    r"some_pattern"
]
"""
TimeOut patterns:
add patterns that should not be said in your chat.
NOT the same as ban patterns.
TimeOut time configurable in config.py
timeout repeats per user configurable in config.py
"""
TO_PAT = [
    r"swear",
    r"some_pattern"
]
