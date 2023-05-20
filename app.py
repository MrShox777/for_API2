import re
import joblib
import requests
import numpy as np
import pandas as pd
import tensorflow as tf
from test2 import correct_spelling
from flask import Flask, jsonify, request
# from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


data = pd.read_csv("santa.csv")

# import logging
# from logging.handlers import RotatingFileHandler


print("1111111111")


app = Flask(__name__)

# logging.basicConfig(filename='access.log', level=logging.INFO)


tokenizer = joblib.load("tmp/model3/tokenizer.joblib")
pad_sequences_ = joblib.load('tmp/model3/pad_sequences.joblib')
label_to_index = joblib.load("tmp/model3/label_to_index.joblib")
loaded_model2 = tf.keras.models.load_model('tmp/model3/model3')


print("2222222222")



def get_top_labels(input_word):
    # Preprocess the input word
    input_word_sequence = tokenizer.texts_to_sequences([input_word])
    input_word_sequence_padded = pad_sequences(input_word_sequence, maxlen=100)

    # Make a prediction with the loaded model
    prediction = loaded_model2.predict(input_word_sequence_padded)

    # Get the top 5 labels
    top_label_indices = prediction.argsort()[0][::-1][:5]
    top_labels = [list(label_to_index.keys())[i] for i in top_label_indices]

    catalogcode = data.loc[data['catalogname'].isin(top_labels), 'p_catalogcode'].unique()[:5]

    results = []
    for i in range(5):
        try:
            result = {}
            result['code'] = top_labels[i]
            result['mixk'] = int(catalogcode[i])
            results.append(result)
        except:
            continue
    return results


@app.route('/org', methods=['POST'])
def org():
    data = request.json
    text = data["text"]
    if (text == "памидор") or (text == "pamidor"):
        text = "памидо"
    if text == "" or text is None:
        return jsonify({"message": "text not found"}), 404
    text = correct_spelling(text=text)
    doc = get_top_labels(text)
    if doc == [{"code": "стеклопакет","mixk": 7003001011000000.0}, {"code": "инсектицид", "mixk": 7008001003000000.0},{"code": "запасные части и аксессуары для автотранспорта","mixk": 8302001008000000.0},{"code": "нижняя петля створки","mixk": 3808001001000000.0},{"code": "прочие запчасти, детали и комплектующие для легковых и грузовых автомобилей","mixk": 8708001374000000.0}]:
        return jsonify({"message": "code not found"}), 500

    return jsonify(doc)


if __name__ == "__main__":
    app.run(host="16.16.203.104", port=80)