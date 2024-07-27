from flask import Flask, render_template, request, jsonify
from main import Cardiac_image_Result , Cardiac_Model , Covid_Model , Image_generator
import io
import tensorflow as tf
import base64
import os
app = Flask(__name__,
            template_folder=os.path.join('..', 'client', 'pages'),
            static_folder=os.path.join('..', 'client', 'static'))

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/go')

@app.route('/get_probab', methods=['POST'])
def predict_probability():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        array = data.get('array')           
        if not array:
            return jsonify({'error': 'Array not provided'}), 400

        predicate = Cardiac_Model.predict(array)
        image = Cardiac_image_Result.get_image(predicate)
        img_str = base64.b64encode(image.getvalue()).decode('utf-8')
        return jsonify({'predicate': predicate , 'image': img_str})
    except Exception as e:
        print("error: ", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST','GET'])
def predict():
        if 'file' not in request.files:
            return jsonify({'error':'No file part'})
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file:
            file_path = "temp/"+file.filename
            file.save(os.path.join("temp", file.filename))
            image = tf.io.read_file(file_path)
            image = tf.image.decode_png(image, channels=3)
            image = tf.image.resize(image, [180, 180])
            image = tf.expand_dims(image, axis=0)
            datagen = Image_generator()
            images = datagen.generate_images(image)
            model = Covid_Model()
            prediction = model.predict(images)
            print(prediction)
            os.remove(file_path)
            return jsonify({'Prediction' : str(prediction)})

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host= '0.0.0.0',   debug=True)
