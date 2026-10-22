# mealprep

A personal Python tool that scales any recipe to your desired serving size and builds a grouped grocery list — organized the way a grocery store is laid out.

Built and maintained by [Suraj Shukla](https://github.com/surajshuklasuraj).

---

## What it does

- Paste a recipe URL from any major cooking site (AllRecipes, Food Network, Serious Eats, and 300+ others)
- Or type in your own recipe ingredients manually
- Set how many servings you want
- Get back a scaled ingredient list with converted units
- Generates a grocery list grouped by store section: Produce, Dairy, Meat & Seafood, Pantry, Spices, Frozen, Other

---

## Why I built this

I meal prep every week and got tired of doing the math manually every time I scale a recipe up or down. I also kept forgetting things at the store because my list was in recipe order, not store order. This tool solves both problems.

---

## Features

- URL-based recipe scraping (via `recipe-scrapers`)
- Ingredient text parsing — pulls out quantity, unit, and ingredient name
- Serving size scaler — scales all quantities proportionally
- Grocery list builder — groups ingredients into store sections
- Save recipes locally to a SQLite database
- Export grocery list to a plain `.txt` file
- Works fully from the command line

---

## Installation

Requires Python 3.10 or higher.

```bash
git clone https://github.com/surajshuklasuraj/mealprep.git
cd mealprep
pip install -r requirements.txt
```

---

## Usage

### Scale a recipe from a URL

```bash
python app.py --url "https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/" --servings 12
```

### Scale a recipe from a text file

```bash
python app.py --file my_recipe.txt --servings 6
```

### Export grocery list to a file

```bash
python app.py --url "https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/" --servings 12 --export
```

### Save a recipe to your local database

```bash
python app.py --url "https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/" --servings 8 --save "Chocolate Chip Cookies"
```

### List saved recipes

```bash
python app.py --list
```

---

## Project structure

```
mealprep/
├── app.py              # Main entry point — CLI interface
├── scraper.py          # Fetches and parses recipe data from URLs
├── scaler.py           # Scales ingredient quantities to new serving size
├── parser.py           # Parses raw ingredient strings into structured data
├── grocery.py          # Groups ingredients into grocery store sections
├── database.py         # SQLite storage for saved recipes
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Planned features

- [ ] Web interface (Flask)
- [ ] Multi-recipe grocery list (combine ingredients from several recipes)
- [ ] Meal planner view — plan the week, auto-generate one combined grocery list
- [ ] Unit conversion (imperial to metric)
- [ ] Ingredient substitution suggestions
- [ ] Pantry tracker — mark what you already have, remove from grocery list

---

## License

MIT License. See [LICENSE](LICENSE) for details.
