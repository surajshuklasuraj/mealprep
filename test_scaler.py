"""
tests/test_scaler.py
Unit tests for the serving size scaler.
Run with: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scaler import scale_ingredients


def make_ingredient(quantity, unit, name):
    display = f"{quantity} {unit} {name}" if unit else f"{quantity} {name}"
    return {'quantity': quantity, 'unit': unit, 'name': name, 'display': display, 'original': display}


class TestScaleIngredients:
    def test_double_servings(self):
        ingredients = [make_ingredient(1.0, 'cup', 'flour')]
        result = scale_ingredients(ingredients, original_servings=4, new_servings=8)
        assert result[0]['quantity'] == 2.0

    def test_halve_servings(self):
        ingredients = [make_ingredient(2.0, 'cups', 'sugar')]
        result = scale_ingredients(ingredients, original_servings=4, new_servings=2)
        assert result[0]['quantity'] == 1.0

    def test_no_quantity_ingredient_kept(self):
        item = {'quantity': None, 'unit': None, 'name': 'salt and pepper', 'display': 'salt and pepper', 'original': 'salt and pepper'}
        result = scale_ingredients([item], original_servings=4, new_servings=8)
        assert result[0]['quantity'] is None
        assert result[0]['display'] == 'salt and pepper'

    def test_scale_ratio(self):
        ingredients = [make_ingredient(3.0, 'tablespoons', 'butter')]
        result = scale_ingredients(ingredients, original_servings=6, new_servings=4)
        assert abs(result[0]['quantity'] - 2.0) < 0.01

    def test_multiple_ingredients(self):
        ingredients = [
            make_ingredient(1.0, 'cup', 'flour'),
            make_ingredient(2.0, 'tablespoons', 'sugar'),
            make_ingredient(0.5, 'cup', 'milk'),
        ]
        result = scale_ingredients(ingredients, original_servings=2, new_servings=6)
        assert result[0]['quantity'] == 3.0
        assert result[1]['quantity'] == 6.0
        assert result[2]['quantity'] == 1.5

    def test_display_is_updated(self):
        ingredients = [make_ingredient(1.0, 'cup', 'flour')]
        result = scale_ingredients(ingredients, original_servings=1, new_servings=3)
        assert '3' in result[0]['display']
        assert 'flour' in result[0]['display']
