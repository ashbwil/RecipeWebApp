from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

# configuration
DEBUG = True

# Final Grocery List
grocery_list = []

# Recipes Added to grocery list
ADDEDRECIPES = []

recipe_dict = {}

recipe_dict[uuid.uuid4().hex] = {
        'title': 'Chili',
        'category': 'Homecooked',
        'meal': 'Dinner',
        'added': False,
        'ingredients': ['Hamburger Meat', 'Onion', 'Taco Seasoning', 'Chili Tomatoes', 'Macaroni noodles',
                        'Saltine Crackers'],
        'directions': """Cook hamburger meat thoroughly and drain. Chop and saute onions, 
                        add onion, taco seasoning and chili tomatoes to pot with meat. 
                        Cook pasta according to directions on box."""
}

recipe_dict[uuid.uuid4().hex] = {
        'title': 'Tacos',
        'category': 'Mexican',
        'meal': 'Dinner',
        'added': False,
        'ingredients': ['Tortillas', 'Onion', 'Tomato', 'Taco Seasoning', 'Hamburger Meat', 'Shredded Cheese', 'salsa'],
        'directions': """Cook hamburger meat, and chop vegetables to bite-sized. Drain meat and add taco seasoning. Warm tortillas in microwave."""
}

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# app route to send new and existing recipes
@app.route('/recipes', methods=['GET', 'POST'])
def recipes_main():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        recipe_dict[uuid.uuid4().hex] = {
            'title': post_data.get('title'),
            'category': post_data.get('category'),
            'meal': post_data.get('meal'),
            'added': post_data.get('added'),
            'ingredients': post_data.get('ingredients'),
            'directions': post_data.get('directions')
        }
        response_object['message'] = 'Recipe added!'
    else:
        # For each recipe, add the key (uuid) as a field alongside the others so js can use it as a key
        recipe_list = []
        for recipe_id, recipe in recipe_dict.items():
            recipe['id'] = recipe_id
            recipe_list.append(recipe)
        response_object['recipes'] = recipe_list
    return jsonify(response_object)

#Edits and deletes recipes
@app.route('/recipes/<recipe_id>', methods=['PUT', 'DELETE'])
def single_recipe(recipe_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        recipe = recipe_dict[recipe_id]
        for element in recipe.keys():
            recipe[element] = post_data.get(element)
        response_object['message'] = 'Recipe Edited!'
    if request.method == 'DELETE':
        remove_recipe(recipe_id)
        response_object['message'] = 'Recipe Removed From Database'
    return jsonify(response_object)

#Sends the ingredient list to vue
@app.route('/ingredients', methods=['GET'])
def send_ingredients():
    print(grocery_list)
    response_object = {'ingredient_list': grocery_list}
    return jsonify(response_object)

#Sends the list of recipes to vue
@app.route('/recipelist', methods=['GET'])
def send_recipes():
    print(ADDEDRECIPES)
    response_object = {'added_recipes': ADDEDRECIPES}
    return jsonify(response_object)

#adds the ingredients and the recipes to main list
@app.route('/addtolist/<recipe_id>', methods=['POST'])
def add_to_recipe_list(recipe_id):
    response_object = {'success': True, "error": None}
    # Lookup the id in the dictionary and add the ingredients to the ingredients list
    if recipe_id in recipe_dict.keys():
        recipe = recipe_dict[recipe_id]
        ADDEDRECIPES.append(recipe['title'])
        grocery_list.extend(recipe['ingredients'])
        return jsonify(response_object)
    response_object['success'] = False
    response_object['error'] = "No recipe id matched. Id: " + recipe_id
    return jsonify(response_object)

#removes things from main list
@app.route('/removefromlist/<recipe_id>', methods=['POST'])
def remove_from_recipe_list(recipe_id):
    response_object = {'success': True, "error": None}
    if recipe_id in recipe_dict.keys():
        recipe = recipe_dict[recipe_id]
        ADDEDRECIPES.remove(recipe['title'])
        for ingredient in recipe['ingredients']:
            grocery_list.remove(ingredient)
        return jsonify(response_object)
    response_object['success'] = False
    response_object['error'] = "No recipe id matched. Id: " + recipe_id
    return jsonify(response_object)


#Removes entire recipe dict
def remove_recipe(recipe_id):
    # TODO if its added to the ingredients list, also remove those ingredients
    if recipe_id in recipe_dict.keys():
        del recipe_dict[recipe_id]
        return True
    return False




if __name__ == '__main__':
    app.run()
