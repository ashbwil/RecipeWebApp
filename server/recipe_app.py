from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

RECIPES = [
    {
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
            'title': post_data.get('title'),
            'category': post_data.get('category'),
            'added': post_data.get('read')
        })
        response_object['message'] = 'Recipe added!'
    else:
        response_object['recipes'] = RECIPES
    return jsonify(response_object)




if __name__ == '__main__':
    app.run()