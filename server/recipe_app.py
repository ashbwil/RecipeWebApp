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
@app.route('/recipes', methods=['GET'])
def recipes_main():
    return jsonify({
        'status': 'success',
        'recipes': RECIPES
    })




if __name__ == '__main__':
    app.run()