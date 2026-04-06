# ------------ EXTERNAL IMPORTS ------------
import re

# ------------ FUNCTION DEFINITION ------------
def parse_version(v):
    """
    Transform a version string into a tuple of integers.

    Example:
    "1.2.3" → (1, 2, 3)
    Note:
    - Extracts ONLY numbers (ignores suffixes like 'rc', 'dev', etc.)
    - This simplifies comparison but does not fully follow PEP 440
    Raises:
    - ValueError: if the version does not contain valid numbers
    """
    nums = re.findall(r'\d+', v)

    if not nums:
        raise ValueError(f"Versión inválida (sin números): '{v}'")
    return tuple(map(int, nums))