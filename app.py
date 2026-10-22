"""
mealprep - Recipe Scaler + Grocery List Builder
Main entry point (CLI)
"""

import argparse
import sys
from scraper import scrape_recipe
from scaler import scale_ingredients
from parser import parse_ingredient_line
from grocery import build_grocery_list, print_grocery_list
from database import save_recipe, list_saved_recipes, get_saved_recipe


def run_from_url(url, servings, save_name=None, export=False):
    print(f"\nFetching recipe from: {url}")
    recipe = scrape_recipe(url)
    if not recipe:
        print("Could not fetch recipe. Check the URL and try again.")
        sys.exit(1)

    print(f"\nRecipe: {recipe['title']}")
    print(f"Original servings: {recipe['servings']}")
    print(f"Scaling to: {servings} servings\n")

    scaled = scale_ingredients(recipe['ingredients'], recipe['servings'], servings)

    print("=" * 50)
    print("SCALED INGREDIENTS")
    print("=" * 50)
    for item in scaled:
        print(f"  {item['display']}")

    print()
    grocery = build_grocery_list(scaled)
    print_grocery_list(grocery)

    if export:
        filename = export_list(recipe['title'], servings, scaled, grocery)
        print(f"\nGrocery list saved to: {filename}")

    if save_name:
        save_recipe(save_name, url, recipe, servings, scaled)
        print(f"\nRecipe saved as: {save_name}")


def run_from_file(filepath, servings, export=False):
    print(f"\nReading recipe from file: {filepath}")
    try:
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(1)

    # Treat the first line as a title if it does not look like an ingredient
    title = lines[0] if lines else "My Recipe"
    ingredient_lines = lines[1:] if lines else []

    # Try to detect original servings from the file (look for "serves X" or "servings: X")
    original_servings = None
    filtered = []
    for line in ingredient_lines:
        lower = line.lower()
        if lower.startswith("serves") or lower.startswith("servings"):
            try:
                original_servings = int(lower.split()[-1])
            except ValueError:
                pass
        else:
            filtered.append(line)
    ingredient_lines = filtered

    if original_servings is None:
        try:
            raw = input("How many servings does this recipe originally make? ").strip()
            original_servings = int(raw)
        except ValueError:
            print("Invalid input. Defaulting to 4 servings.")
            original_servings = 4

    parsed = [parse_ingredient_line(line) for line in ingredient_lines]
    scaled = scale_ingredients(parsed, original_servings, servings)

    print(f"\nRecipe: {title}")
    print(f"Original servings: {original_servings} -> Scaled to: {servings}\n")

    print("=" * 50)
    print("SCALED INGREDIENTS")
    print("=" * 50)
    for item in scaled:
        print(f"  {item['display']}")

    print()
    grocery = build_grocery_list(scaled)
    print_grocery_list(grocery)

    if export:
        filename = export_list(title, servings, scaled, grocery)
        print(f"\nGrocery list saved to: {filename}")


def export_list(title, servings, scaled, grocery):
    safe_title = title.replace(" ", "_").replace("/", "-")[:40]
    filename = f"grocery_{safe_title}_{servings}servings.txt"
    with open(filename, 'w') as f:
        f.write(f"Grocery List: {title} ({servings} servings)\n")
        f.write("=" * 50 + "\n\n")
        for section, items in grocery.items():
            if items:
                f.write(f"{section.upper()}\n")
                for item in items:
                    f.write(f"  - {item['display']}\n")
                f.write("\n")
    return filename


def main():
    parser = argparse.ArgumentParser(
        description="mealprep: Scale any recipe and build a grocery list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app.py --url "https://www.allrecipes.com/recipe/10813/" --servings 8
  python app.py --file my_recipe.txt --servings 4
  python app.py --url "https://..." --servings 6 --export
  python app.py --url "https://..." --servings 4 --save "Pasta Bake"
  python app.py --list
        """
    )

    parser.add_argument("--url", help="URL of the recipe to scrape")
    parser.add_argument("--file", help="Path to a plain text recipe file")
    parser.add_argument("--servings", type=int, default=4, help="Number of servings to scale to (default: 4)")
    parser.add_argument("--save", metavar="NAME", help="Save the recipe to local database with this name")
    parser.add_argument("--load", metavar="NAME", help="Load and re-scale a previously saved recipe")
    parser.add_argument("--list", action="store_true", help="List all saved recipes")
    parser.add_argument("--export", action="store_true", help="Export the grocery list to a .txt file")

    args = parser.parse_args()

    if args.list:
        recipes = list_saved_recipes()
        if not recipes:
            print("No saved recipes found.")
        else:
            print("\nSaved recipes:")
            for r in recipes:
                print(f"  - {r['name']}  (saved {r['saved_at']})")
        return

    if args.load:
        recipe_data = get_saved_recipe(args.load)
        if not recipe_data:
            print(f"No saved recipe found with name: {args.load}")
            sys.exit(1)
        run_from_url(recipe_data['url'], args.servings, export=args.export)
        return

    if args.url:
        run_from_url(args.url, args.servings, save_name=args.save, export=args.export)
    elif args.file:
        run_from_file(args.file, args.servings, export=args.export)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
