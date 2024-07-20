# from flask import Flask, render_template, request, jsonify
# from main import Model , Result
# import base64
# app = Flask(__name__, template_folder='pages', static_folder='static')

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/get_probab', methods=['POST'])
# def predict_probability():
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({'error': 'No input data provided'}), 400

#         array = data.get('array')           
#         if not array:
#             return jsonify({'error': 'Array not provided'}), 400

#         predicate = Model.predict(array)
#         image = Result.get_image(predicate)
#         img_str = base64.b64encode(image.getvalue()).decode('utf-8')
#         return jsonify({'predicate': predicate , 'image': img_str})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(port=3000 , debug=True)
from flask import Flask, render_template, request, jsonify
from main import Model, Result
import base64

app = Flask(__name__, template_folder='pages', static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_probab', methods=['POST'])
def predict_probability():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        array = data.get('array')
        if not array:
            return jsonify({'error': 'Array not provided'}), 400

        # Assuming Model.predict() and Result.get_image() are correctly implemented
        predicate = Model.predict(array)
        image = Result.get_image(predicate)

        # Encode image to base64
        img_str = base64.b64encode(image.getvalue()).decode('utf-8')

        return jsonify({'predicate': predicate, 'image': img_str})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # In production, use a production-ready WSGI server like Gunicorn
    # Example command to run with Gunicorn: gunicorn -w 4 -b 0.0.0.0:3000 your_module_name:app
    app.run(port=3000, debug=False)
