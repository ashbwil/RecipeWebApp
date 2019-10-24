from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid


# configuration
DEBUG = True

#Final Grocery List
LIST = []

#Recipes Added to grocery list
ADDEDRECIPES = []

#List of Dictionaries holding recipe info
RECIPES = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Chili',
        'category': 'Homecooked',
        'meal': 'Dinner',
        'added': False,
        'ingredients': ['Hamburger Meat', 'Onion', 'Taco Seasoning', 'Chili Tomatoes']
    }
]

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


#app route to main page
@app.route('/recipes', methods=['GET', 'POST'])
def recipes_main():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        RECIPES.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'category': post_data.get('category'),
            'meal': post_data.get('meal'),
            'added': post_data.get('added'),
            'ingredients': post_data.get('ingredients')
        })
        response_object['message'] = 'Recipe added!'
    else:
        response_object['recipes'] = RECIPES
    return jsonify(response_object)


@app.route('/recipes/<recipe_id>', methods=['PUT', 'DELETE'])
def single_recipe(recipe_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_success = remove_recipe(recipe_id)
        if remove_success:
            RECIPES.append({
                'id': uuid.uuid4().hex,
                'title': post_data.get('title'),
                'category': post_data.get('category'),
                'meal': post_data.get('meal'),
                'added': post_data.get('added'),
                'ingredients': post_data.get('ingredients')
            })
            response_object['message'] = 'Recipe Edited!'
    if request.method == 'DELETE':
        remove_recipe(recipe_id)
        response_object['message'] = 'Recipe Removed From Database'
    return jsonify(response_object)

@app.route('/ingredients', methods=['GET'])
def send_ingredients():
    response_object = {'ingredient_list': LIST}
    return jsonify(response_object)


def remove_recipe(recipe_id):
    for recipe in RECIPES:
        if recipe['id'] == recipe_id:
            RECIPES.remove(recipe)
            return True
    return False

def add_to_list():
    for recipe in RECIPES:
        if recipe['added']:
            LIST.extend(recipe['ingredients'])


add_to_list()
print(LIST)




if __name__ == '__main__':
    app.run()