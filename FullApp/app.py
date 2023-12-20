import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import jsonify

app = Flask(__name__)

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

def dummy_chatbot_response(message):
    # Replace this with your chatbot logic
    return "Echo: " + message

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/process_chat', methods=['POST'])
def process_chat():
    message = request.json['message']
    response = dummy_chatbot_response(message)
    return jsonify({"response": response})


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('chat_page'))

if __name__ == '__main__':
    app.run(debug=True)
