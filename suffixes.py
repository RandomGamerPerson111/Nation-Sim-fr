def SN(num):
    
    num = float(f'{num:.3g}')
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return f'{num:f}'.rstrip('0').rstrip('.') + ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx'][magnitude]

def SNS(num):
    
    num = float(f'{num:.6g}')
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return f'{num:3f}'.rstrip('0').rstrip('.') + ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx'][magnitude]

import re

def ISN(s):
    s = str(s).strip().upper()
    if not s:
        return None

    # Define magnitude multipliers
    multipliers = {
        'K': 1000,
        'M': 1000000,
        'B': 1000000000,
        'T': 1000000000000,
        'QA': 1000000000000000,
        'QI': 1000000000000000000,
        'SX': 1000000000000000000000,
    }
    
    # Get the list of suffixes for the regex pattern
    suffix_pattern = '|'.join(multipliers.keys())
    
    # Use regular expression to find numbers with optional suffixes
    match = re.fullmatch(fr"(\d+\.?\d*)\s*({suffix_pattern})", s)
    
    if match:
        number_part = float(match.group(1))
        suffix = match.group(2)
        return number_part * multipliers[suffix]

    # Fallback for standard numbers with no suffixes
    try:
        if '.' in s:
            return float(s)
        else:
            return int(s)
    except ValueError:
        return None

