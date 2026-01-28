from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Load dataset (FIXED PATH)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'IndianFoodDataset.csv')

df = pd.read_csv(DATA_PATH)

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/style.css')
def serve_css():
    return send_from_directory('../frontend', 'style.css')

@app.route('/get_recipes', methods=['POST'])
def get_recipes():
    data = request.json

    dish_name_filter = data.get('dish_name', '').lower().strip()

    user_ingredients = data.get('ingredients', '').lower().split(',')
    user_ingredients = [i.strip() for i in user_ingredients if i.strip()]

    servings_filter = data.get('servings', '').strip()
    cuisine_filter = data.get('cuisine', '').strip()
    course_filter = data.get('course', '').strip()
    diet_filter = data.get('diet', '').strip()

    matched_recipes = []

    for _, row in df.iterrows():
        recipe_name = str(row['RecipeName']).lower()
        recipe_ingredients = str(row['Ingredients']).lower()

        if dish_name_filter and dish_name_filter not in recipe_name:
            continue

        if user_ingredients and not all(ing in recipe_ingredients for ing in user_ingredients):
            continue

        if servings_filter and str(row.get('Servings', '')).strip() != servings_filter:
            continue
        if cuisine_filter and str(row.get('Cuisine', '')).strip() != cuisine_filter:
            continue
        if course_filter and str(row.get('Course', '')).strip() != course_filter:
            continue
        if diet_filter and str(row.get('Diet', '')).strip() != diet_filter:
            continue

        matched_recipes.append({
            "name": row['RecipeName'],
            "ingredients": row['Ingredients'],
            "prep_time": row.get('PrepTimeInMins', ''),
            "cook_time": row.get('CookTimeInMins', ''),
            "total_time": row.get('TotalTimeInMins', ''),
            "servings": row.get('Servings', ''),
            "cuisine": row.get('Cuisine', ''),
            "course": row.get('Course', ''),
            "diet": row.get('Diet', ''),
            "instructions": row['Instructions']
        })

    return jsonify(matched_recipes)

if __name__ == '__main__':
    app.run(debug=True)
