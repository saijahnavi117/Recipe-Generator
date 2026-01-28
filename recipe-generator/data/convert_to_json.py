import pandas as pd
import json

# Load CSV file
df = pd.read_csv("IndianFoodDataset.csv")  # Make sure the CSV is in data/

recipes = []

for _, row in df.iterrows():
    title = row.get('RecipeName') or row.get('title')
    ingredients = row.get('Ingredients') or row.get('ingredients')
    instructions = row.get('Instructions') or row.get('instructions')

    # Skip rows with missing data
    if pd.isna(title) or pd.isna(ingredients) or pd.isna(instructions):
        continue

    # Convert ingredients & instructions to lists
    ingredients_list = [i.strip().lower() for i in ingredients.split(',')] if isinstance(ingredients, str) else []
    instructions_list = [i.strip() for i in instructions.split('.') if i.strip()] if isinstance(instructions, str) else []

    recipes.append({
        "title": title.strip(),
        "ingredients": ingredients_list,
        "instructions": instructions_list
    })

# Save as JSON
with open("recipes.json", "w", encoding='utf-8') as f:
    json.dump(recipes, f, indent=2, ensure_ascii=False)

print(f"Converted {len(recipes)} recipes to recipes.json")
