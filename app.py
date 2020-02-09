from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array

imge = None
UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_image(fname):
    img = load_img(fname, color_mode='grayscale', target_size=(28, 28))
    img = img_to_array(img)
    # plt.imshow(img)
    img = img.reshape(1, 28, 28, 1)
    img = img.astype('float32') / 255

    return img

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    global imge
    imge = filename
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/result')
def predict():
    global imge
    model = models.load_model('model.h5')
    img = load_image('images\\' + imge)
    pred = model.predict_classes(img)

    return (render_template('result.html', sum123=pred[0]))




if __name__ == '__main__':
    app.run()
