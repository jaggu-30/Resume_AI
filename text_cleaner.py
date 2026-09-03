import re


def clean_text(text):
    """
    Clean and normalize extracted resume text.
    """

    # Convert to lowercase
    text = text.lower()

    # Normalize common technical terms
    text = text.replace("c ++", "c++")
    text = text.replace("c #", "c#")
    text = text.replace(". net", ".net")

    # Replace bullet characters
    text = re.sub(r"[•●▪◦]", " ", text)

    # Remove unnecessary special characters
    # Keep technical symbols such as +, #, ., / and -
    text = re.sub(r"[^a-z0-9+#./\-\s]", " ", text)

    # Replace multiple spaces/newlines/tabs with one space
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary spaces around technical symbols
    text = re.sub(r"\s*([+/.#-])\s*", r"\1", text)

    return text.strip()