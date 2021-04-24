def add_upper_reserved_words(reserved_words):
    upper_reserved_words = [word.upper() for word in reserved_words]
    return reserved_words + upper_reserved_words