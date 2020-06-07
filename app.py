from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "uploads/"

# https://pythonbasics.org/flask-upload-file/
# TODO add max size in bytes
# app.config['MAX_CONTENT_PATH'] = 8000

@app.route("/")
def index():
  return render_template('upload.html')

@app.route("/resize/", methods = ['GET', 'POST'])
def resize():
  try:
    width = int(request.args.get('width'))
    height = int(request.args.get('height'))

    f = request.files['image']
    image_filename = f.save(
      os.path.join(app.config['UPLOAD_FOLDER'], 
      secure_filename(f.filename))
    )
    print(image_filename)

    return 'file uploaded successfully'
  except ValueError:
    return "Make sure width and height are numbers"
  return "Hello World!"

if __name__ == "__main__":
  app.run(debug=True)

