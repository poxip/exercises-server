"""
    API server helpers
"""

def normalize(text):
    """Normalize specified string

    :param str text: A string to be normalized
    :return Normalized string or empty string if text argument is not a string
    """
    if not isinstance(text, str):
        return ''

    return text.lower().strip()