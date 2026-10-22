"""
scraper.py
Fetches a recipe from a URL using recipe-scrapers and returns
a normalised dict with title, servings, and a list of ingredient strings.
"""

from parser import parse_ingredient_line


def scrape_recipe(url):
    """
    Scrape a recipe URL and return a dict:
      {
        'title': str,
        'servings': int,
        'ingredients': [ {quantity, unit, name, display} ... ]
      }
    Returns None on failure.
    """
    try:
        from recipe_scrapers import scrape_me
    except ImportError:
        print("recipe-scrapers is not installed. Run: pip install recipe-scrapers")
        return None

    try:
        scraper = scrape_me(url)
    except Exception as e:
        print(f"Error fetching recipe: {e}")
        return None

    try:
        title = scraper.title() or "Untitled Recipe"
    except Exception:
        title = "Untitled Recipe"

    try:
        raw_servings = scraper.yields()
        # yields() returns a string like "4 servings" or just "4"
        servings = int(''.join(filter(str.isdigit, str(raw_servings)))) or 4
    except Exception:
        servings = 4

    try:
        raw_ingredients = scraper.ingredients()
    except Exception:
        raw_ingredients = []

    ingredients = [parse_ingredient_line(line) for line in raw_ingredients if line.strip()]

    return {
        'title': title,
        'servings': servings,
        'ingredients': ingredients,
    }
