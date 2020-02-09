from flask import Flask, render_template
import tensorflow as tf
from tensorflow.keras.datasets import mnist
(train_images, train_labels),(test_images, test_labels) = mnist.load_data()

from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', sum123=98)


if __name__ == '__main__':
    app.run()
