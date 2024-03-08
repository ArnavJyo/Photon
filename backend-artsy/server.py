from flask import Flask, request, jsonify
from flask_cors import CORS
from distance_metric import euclidian_distance,minkowski_distance,manhattan_distance,chebyshev_distance
app = Flask(__name__)
CORS(app)
@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    temp_image_path = 'C:/Users/arnav/Desktop/artsy/data/image-test.png'
    image_file.save(temp_image_path)
    button_text = request.form.get('buttonText')
    if button_text == "Euclidean":
        processed_image_path = euclidian_distance(temp_image_path)
    elif button_text == "Minkowski":
        processed_image_path = minkowski_distance(temp_image_path)
    elif button_text == "Manhattan":
        processed_image_path = manhattan_distance(temp_image_path)
    elif button_text == "Chebyshev":
        processed_image_path = chebyshev_distance(temp_image_path)
    else:
        return jsonify({'error': 'Invalid button text'}), 400
    

    return jsonify({'processed_image_path': processed_image_path.tolist()})

if __name__ == '__main__':
    app.run(debug=True,port=5000)
