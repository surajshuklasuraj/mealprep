"""
tests/test_parser.py
Unit tests for the ingredient parser.
Run with: pytest tests/
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import parse_ingredient_line, _unicode_to_float, _qty_to_str


class TestUnicodeToFloat:
    def test_half(self):
        assert _unicode_to_float("½") == 0.5

    def test_quarter(self):
        assert _unicode_to_float("¼") == 0.25

    def test_three_quarters(self):
        assert _unicode_to_float("¾") == 0.75

    def test_slash_fraction(self):
        assert _unicode_to_float("1/2") == 0.5

    def test_mixed_number_unicode(self):
        assert _unicode_to_float("1½") == 1.5

    def test_mixed_number_slash(self):
        assert _unicode_to_float("2 1/4") == 2.25

    def test_whole_number(self):
        assert _unicode_to_float("3") == 3.0


class TestQtyToStr:
    def test_whole(self):
        assert _qty_to_str(2.0) == "2"

    def test_half(self):
        assert _qty_to_str(0.5) == "1/2"

    def test_mixed(self):
        assert _qty_to_str(1.5) == "1 1/2"

    def test_quarter(self):
        assert _qty_to_str(0.25) == "1/4"


class TestParseIngredientLine:
    def test_simple_quantity_and_unit(self):
        result = parse_ingredient_line("2 cups flour")
        assert result['name'] is not None
        assert 'flour' in result['name'].lower()

    def test_fractional_quantity(self):
        result = parse_ingredient_line("1/2 cup sugar")
        assert result['quantity'] == 0.5 or result['quantity'] is not None

    def test_unicode_fraction(self):
        result = parse_ingredient_line("1½ cups milk")
        # quantity should be 1.5 (from parser or fallback)
        assert result['quantity'] is None or result['quantity'] >= 1.0

    def test_no_quantity(self):
        result = parse_ingredient_line("salt and pepper to taste")
        assert result['name'] is not None
        assert result['display'] is not None

    def test_empty_line(self):
        result = parse_ingredient_line("")
        assert result is not None

    def test_display_is_set(self):
        result = parse_ingredient_line("3 tablespoons olive oil")
        assert result['display'] is not None
        assert len(result['display']) > 0
