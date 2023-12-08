"""
eec.py
---
Excla! Error Codes module.
"""

def file_not_found():
    """EEC File Not Found
    ---
    Used for handling opening a non-existent .json file.

    Returns
    ---
    EEC 110 (converted to HEX 0x6E for convenience) and more info about the error.
    """
    return "[EEC0x6E] // Could not fetch resource, please contact an administrator."