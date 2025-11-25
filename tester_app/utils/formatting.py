def smart_title(name: str) -> str:
    """
    Converts uppercase region names to proper title case,
    keeping known acronyms like DKI, DIY, NTB, NTT fully uppercase.
    """
    if not name:
        return name

    # Known acronyms in Indonesian regions
    acronyms = {"DKI", "DIY", "NAD", "NTB", "NTT", "KEP", "RIAU", "MALUKU"}

    words = name.split()
    formatted = []

    for word in words:
        word_upper = word.upper()

        # If it's a known acronym, keep it uppercase
        if word_upper in acronyms:
            formatted.append(word_upper)
        # If it's a prefix like "KEPULAUAN" (not an acronym but usually normal case)
        else:
            formatted.append(word.capitalize())

    return " ".join(formatted)
