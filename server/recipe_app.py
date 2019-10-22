from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid


# configuration
DEBUG = True

RECIPES = [
    {
        'id': uuid.uuid4().hex,
        'title': 'Chilli',
        'category': 'Dinner',
        'added': True
    }
]

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/recipes', methods=['GET', 'POST'])
def recipes_main():
    response_object = {'status': 'success'}
    if request.method =='POST':
        post_data = request.get_json()
        RECIPES.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'category': post_data.get('category'),
            'added': post_data.get('added')
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
                'added': post_data.get('added')
            })
            response_object['message'] = 'Recipe Edited!'
    if request.method == 'DELETE':
        remove_recipe(recipe_id)
        response_object['message'] = 'Recipe Removed From Database'
    return jsonify(response_object)


def remove_recipe(recipe_id):
    for recipe in RECIPES:
        if recipe['id'] == recipe_id:
            RECIPES.remove(recipe)
            return True
    return False


if __name__ == '__main__':
    app.run()