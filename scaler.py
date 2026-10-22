"""
scaler.py
Scales a list of parsed ingredient dicts from original_servings to new_servings.
"""

from parser import _qty_to_str


def scale_ingredients(ingredients, original_servings, new_servings):
    """
    Takes a list of ingredient dicts (from parser.py) and scales quantities.

    Returns a new list of ingredient dicts with updated quantity and display fields.
    """
    if original_servings <= 0:
        original_servings = 1

    ratio = new_servings / original_servings

    scaled = []
    for item in ingredients:
        new_item = dict(item)  # copy

        if item.get('quantity') is not None:
            new_qty = item['quantity'] * ratio
            new_item['quantity'] = new_qty
            new_item['display'] = _build_display(new_qty, item.get('unit'), item.get('name'), item.get('original', ''))
        else:
            # No numeric quantity — keep as-is (e.g. "salt and pepper to taste")
            new_item['display'] = item.get('display') or item.get('original') or item.get('name', '')

        scaled.append(new_item)

    return scaled


def _build_display(quantity, unit, name, original):
    qty_str = _qty_to_str(quantity)
    if not name:
        return original
    if unit:
        return f"{qty_str} {unit} {name}"
    return f"{qty_str} {name}"
