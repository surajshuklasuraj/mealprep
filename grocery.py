"""
grocery.py
Groups a list of scaled ingredient dicts into grocery store sections
and prints a formatted grocery list.
"""

# Keywords used to classify each ingredient into a store section.
# Order matters: first match wins.
SECTION_KEYWORDS = {
    "Produce": [
        "apple", "banana", "berry", "berries", "strawberr", "blueberr", "raspberr",
        "lemon", "lime", "orange", "avocado", "tomato", "tomatoes",
        "lettuce", "spinach", "kale", "arugula", "cabbage", "broccoli",
        "cauliflower", "carrot", "celery", "cucumber", "zucchini", "squash",
        "bell pepper", "pepper", "onion", "garlic", "shallot", "leek",
        "mushroom", "potato", "sweet potato", "yam", "corn", "asparagus",
        "green bean", "pea", "snap pea", "edamame", "beet", "radish",
        "turnip", "parsnip", "fennel", "artichoke", "ginger", "fresh herb",
        "cilantro", "parsley", "basil", "rosemary", "thyme", "mint",
        "scallion", "chive", "jalape", "serrano", "mango", "pineapple",
        "grape", "peach", "plum", "pear",
    ],
    "Meat & Seafood": [
        "chicken", "beef", "pork", "lamb", "turkey", "duck", "veal",
        "ground beef", "ground turkey", "ground pork", "steak", "ribs",
        "sausage", "bacon", "ham", "salami", "pepperoni", "chorizo",
        "salmon", "tuna", "shrimp", "prawn", "cod", "tilapia", "halibut",
        "crab", "lobster", "clam", "mussel", "oyster", "scallop",
        "anchovy", "sardine",
    ],
    "Dairy & Eggs": [
        "milk", "cream", "half and half", "butter", "ghee",
        "cheese", "cheddar", "mozzarella", "parmesan", "brie", "feta",
        "ricotta", "cottage cheese", "cream cheese", "sour cream",
        "yogurt", "egg", "eggs",
        "heavy cream", "whipping cream",
    ],
    "Bakery & Bread": [
        "bread", "baguette", "roll", "bun", "tortilla", "pita",
        "naan", "croissant", "bagel", "muffin", "puff pastry",
        "pie crust", "phyllo",
    ],
    "Frozen": [
        "frozen", "ice cream", "gelato", "sorbet",
        "frozen pea", "frozen corn", "frozen berry",
    ],
    "Canned & Jarred": [
        "canned", "can of", "jar of", "tomato paste", "tomato sauce",
        "crushed tomatoes", "diced tomatoes", "coconut milk", "coconut cream",
        "chicken broth", "beef broth", "vegetable broth", "stock",
        "chickpeas", "kidney beans", "black beans", "lentils", "cannellini",
        "olives", "capers", "pickles", "artichoke hearts", "roasted peppers",
        "pumpkin puree", "apple sauce",
    ],
    "Pasta, Rice & Grains": [
        "pasta", "spaghetti", "penne", "rigatoni", "fettuccine", "linguine",
        "lasagna", "orzo", "couscous", "rice", "brown rice", "wild rice",
        "quinoa", "farro", "barley", "oats", "oatmeal", "polenta", "grits",
        "noodle", "ramen", "udon", "soba",
    ],
    "Baking": [
        "flour", "all-purpose flour", "bread flour", "cake flour",
        "sugar", "brown sugar", "powdered sugar", "confectioners",
        "baking powder", "baking soda", "yeast", "cocoa", "chocolate chip",
        "vanilla extract", "almond extract", "cornstarch", "arrowroot",
        "gelatin", "honey", "maple syrup", "molasses", "corn syrup",
    ],
    "Spices & Condiments": [
        "salt", "pepper", "paprika", "cayenne", "cumin", "coriander",
        "turmeric", "cinnamon", "nutmeg", "cloves", "cardamom", "allspice",
        "oregano", "thyme", "rosemary", "bay leaf", "bay leaves",
        "chili powder", "curry powder", "garam masala", "smoked paprika",
        "garlic powder", "onion powder", "dried", "seasoning", "spice",
        "soy sauce", "fish sauce", "worcestershire", "hot sauce", "sriracha",
        "ketchup", "mustard", "mayonnaise", "vinegar", "olive oil",
        "vegetable oil", "canola oil", "sesame oil", "coconut oil",
        "cooking spray",
    ],
    "Nuts, Seeds & Dried Fruit": [
        "almond", "walnut", "pecan", "cashew", "peanut", "pine nut",
        "pistachio", "hazelnut", "macadamia", "sesame seed", "sunflower seed",
        "pumpkin seed", "chia seed", "flax seed", "raisin", "cranberr",
        "dried cherry", "dried apricot", "dried mango", "coconut flake",
    ],
    "Beverages": [
        "wine", "beer", "broth", "juice", "coffee", "tea",
        "water", "sparkling", "soda", "lemonade",
    ],
}


def classify_ingredient(name):
    """Return the grocery section for an ingredient name string."""
    name_lower = (name or "").lower()
    for section, keywords in SECTION_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                return section
    return "Other"


def build_grocery_list(scaled_ingredients):
    """
    Group a list of scaled ingredient dicts into sections.
    Returns a dict: { section_name: [ingredient_dict, ...] }
    """
    sections = {section: [] for section in SECTION_KEYWORDS}
    sections["Other"] = []

    for item in scaled_ingredients:
        section = classify_ingredient(item.get('name', ''))
        sections[section].append(item)

    # Remove empty sections
    return {k: v for k, v in sections.items() if v}


def print_grocery_list(grocery):
    """Print a formatted grocery list grouped by section."""
    print("=" * 50)
    print("GROCERY LIST (by store section)")
    print("=" * 50)

    for section, items in grocery.items():
        if items:
            print(f"\n{section.upper()}")
            print("-" * len(section))
            for item in items:
                print(f"  [ ]  {item['display']}")

    print()
