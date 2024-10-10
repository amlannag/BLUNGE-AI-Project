from flask import Flask, request, send_file
from transformers import pipeline
from PIL import Image
import io
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS


pipe = pipeline("image-segmentation", model="briaai/RMBG-1.4", trust_remote_code=True)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    
    if 'image' not in request.files:
        return "No image uploaded", 400

   
    file = request.files['image']
    image = Image.open(file)

   
    pillow_image = pipe(image, return_mask=False)  

    
    img_io = io.BytesIO()
    pillow_image.save(img_io, 'PNG')
    img_io.seek(0)

   
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
