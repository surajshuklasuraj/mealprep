"""
parser.py
Parses a raw ingredient string like "1½ cups all-purpose flour, sifted"
into a structured dict: { quantity, unit, name, display }

Uses ingredient-parser-nlp when available, with a simple regex fallback.
"""

import re

# Unicode fraction map
UNICODE_FRACTIONS = {
    '¼': 0.25,   # ¼
    '½': 0.5,    # ½
    '¾': 0.75,   # ¾
    '⅓': 1/3,    # ⅓
    '⅔': 2/3,    # ⅔
    '⅕': 0.2,    # ⅕
    '⅖': 0.4,    # ⅖
    '⅗': 0.6,    # ⅗
    '⅘': 0.8,    # ⅘
    '⅙': 1/6,    # ⅙
    '⅚': 5/6,    # ⅚
    '⅛': 0.125,  # ⅛
    '⅜': 0.375,  # ⅜
    '⅝': 0.625,  # ⅝
    '⅞': 0.875,  # ⅞
}

COMMON_UNITS = [
    'tablespoons', 'tablespoon', 'tbsp', 'tbsps',
    'teaspoons', 'teaspoon', 'tsp', 'tsps',
    'cups', 'cup',
    'ounces', 'ounce', 'oz',
    'pounds', 'pound', 'lb', 'lbs',
    'grams', 'gram', 'g',
    'kilograms', 'kilogram', 'kg',
    'milliliters', 'milliliter', 'ml',
    'liters', 'liter', 'l',
    'fluid ounces', 'fluid ounce', 'fl oz',
    'quarts', 'quart', 'qt',
    'pints', 'pint', 'pt',
    'gallons', 'gallon', 'gal',
    'inches', 'inch', 'in',
    'cloves', 'clove',
    'stalks', 'stalk',
    'slices', 'slice',
    'sprigs', 'sprig',
    'bunches', 'bunch',
    'cans', 'can',
    'packages', 'package', 'pkg',
    'pieces', 'piece',
    'pinch', 'pinches',
    'dash', 'dashes',
    'handfuls', 'handful',
    'heads', 'head',
]


def _unicode_to_float(text):
    """Replace unicode fractions and slash fractions with float equivalents."""
    result = 0.0
    text = text.strip()

    for char, val in UNICODE_FRACTIONS.items():
        if char in text:
            text = text.replace(char, f' {val} ')

    # Handle "1 1/2" or "1/2" style
    parts = text.split()
    for part in parts:
        if '/' in part:
            try:
                num, den = part.split('/')
                result += float(num) / float(den)
            except (ValueError, ZeroDivisionError):
                pass
        else:
            try:
                result += float(part)
            except ValueError:
                pass

    return result if result > 0 else None


def _fallback_parse(line):
    """Simple regex-based ingredient parser as a fallback."""
    line = line.strip()
    original = line

    # Pattern: optional number (int, float, fraction, unicode fraction) + optional unit + rest
    number_pattern = r'[\d¼½¾⅓-⅞][\d\s\./¼½¾⅓-⅞]*'
    unit_pattern = '|'.join(sorted(COMMON_UNITS, key=len, reverse=True))

    quantity = None
    unit = None
    name = line

    # Try to extract quantity
    m = re.match(rf'^({number_pattern})', line)
    if m:
        raw_qty = m.group(1).strip()
        quantity = _unicode_to_float(raw_qty)
        remainder = line[m.end():].strip()

        # Try to extract unit
        unit_match = re.match(rf'^({unit_pattern})\b\.?\s*', remainder, re.IGNORECASE)
        if unit_match:
            unit = unit_match.group(1).lower()
            name = remainder[unit_match.end():].strip()
        else:
            name = remainder
    else:
        name = line

    # Clean up name (remove leading comma, "of", etc.)
    name = re.sub(r'^(of\s+)', '', name, flags=re.IGNORECASE)
    name = name.lstrip(',').strip()

    display = _format_display(quantity, unit, name) if quantity else original

    return {
        'quantity': quantity,
        'unit': unit,
        'name': name if name else original,
        'display': display,
        'original': original,
    }


def _format_display(quantity, unit, name):
    if quantity is None:
        return name
    qty_str = _qty_to_str(quantity)
    if unit:
        return f"{qty_str} {unit} {name}"
    return f"{qty_str} {name}"


def _qty_to_str(qty):
    if qty is None:
        return ""
    if qty == int(qty):
        return str(int(qty))
    # Common fractions
    fracs = {0.25: '1/4', 0.5: '1/2', 0.75: '3/4', 1/3: '1/3', 2/3: '2/3',
             0.125: '1/8', 0.375: '3/8', 0.625: '5/8', 0.875: '7/8'}
    # Handle mixed numbers like 1.5 -> "1 1/2"
    whole = int(qty)
    frac = round(qty - whole, 4)
    frac_str = fracs.get(frac)
    if whole > 0 and frac_str:
        return f"{whole} {frac_str}"
    if frac_str:
        return frac_str
    return f"{qty:.2f}".rstrip('0').rstrip('.')


def parse_ingredient_line(line):
    """
    Parse one ingredient line.
    Tries ingredient-parser-nlp first; falls back to regex parser.
    """
    if not line or not line.strip():
        return {'quantity': None, 'unit': None, 'name': line, 'display': line, 'original': line}

    try:
        from ingredient_parser import parse_ingredient
        result = parse_ingredient(line)

        # ingredient-parser-nlp returns a ParsedIngredient object
        qty = None
        unit = None
        name = None

        # Amount
        if hasattr(result, 'amount') and result.amount:
            amounts = result.amount if isinstance(result.amount, list) else [result.amount]
            total = 0.0
            unit_val = None
            for amt in amounts:
                if hasattr(amt, 'quantity') and amt.quantity is not None:
                    try:
                        total += float(str(amt.quantity))
                    except (ValueError, TypeError):
                        pass
                if hasattr(amt, 'unit') and amt.unit and not unit_val:
                    unit_val = str(amt.unit)
            qty = total if total > 0 else None
            unit = unit_val

        # Name
        if hasattr(result, 'name') and result.name:
            if isinstance(result.name, list):
                name = ' '.join([str(n) for n in result.name])
            else:
                name = str(result.name)

        if not name:
            name = line

        display = _format_display(qty, unit, name) if qty else line

        return {
            'quantity': qty,
            'unit': unit,
            'name': name,
            'display': display,
            'original': line,
        }

    except (ImportError, Exception):
        return _fallback_parse(line)
