from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from PIL import Image


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads/"

# https://pythonbasics.org/flask-upload-file/
# TODO add max size in bytes
# app.config['MAX_CONTENT_PATH'] = 8000

def append_local_upload_dir(filename):
  return os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))


@app.route("/")
def index():
  return render_template('upload.html')

@app.route("/resize/", methods = ['GET', 'POST'])
def resize():
  try:
    width = int(request.args.get('width'))
    height = int(request.args.get('height'))

    f = request.files['image']

    img_file_loc = append_local_upload_dir(f.filename) 
    f.save(img_file_loc)

    img_to_resize = Image.open(img_file_loc)
    resized_img = img_to_resize.resize((width, height))
    resized_img.save(img_file_loc, "PNG", optimize=True)

    return 'file uploaded successfully'
    
  except ValueError:
    return "Make sure width and height are numbers"
  return "Hello World!"

if __name__ == "__main__":
  app.run(debug=True)

