from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

RECIPES = [
    {
        'Name:': 'Chilli',
        'Category': 'Dinner',
        'Added': True
    }
]

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/recipes', methods=['GET', 'POST'])
def main_page():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        RECIPES.append({
            'Name': post_data.get('Name'),
            'Category': post_data.get('Category'),
            'Added': post_data.get('Added')
        })
        response_object['message'] = 'Recipe Added!'
    else:
        response_object['recipes'] = 'RECIPES'
    return jsonify(response_object)




if __name__ == '__main__':
    app.run()