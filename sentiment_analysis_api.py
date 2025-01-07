# from flask import Flask, request, jsonify, send_file
# import pandas as pd
# import re
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import pickle

# app = Flask(__name__)

# model = load_model("sentiment_model.h5")
# with open("tokenizer.pkl", "rb") as f:
#     word_tokenizer = pickle.load(f)

# vocab_size = 5000
# max_len = 100

# def preprocess_text(sen):
#     TAG_RE = re.compile(r'<[^>]+>')
#     sentence = TAG_RE.sub('', sen)
#     sentence = re.sub('[^a-zA-Z]', ' ', sentence)
#     sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
#     sentence = re.sub(r'\s+', ' ', sentence)
#     sentence = sentence.lower()
#     return sentence

# @app.route('/predict', methods=['POST'])
# def predict_sentiment():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     if not file.filename.endswith('.xlsx'):
#         return jsonify({"error": "Invalid file format. Please upload an Excel file"}), 400

#     try:
#         new_reviews = pd.read_excel(file)
#     except Exception as e:
#         return jsonify({"error": f"Error reading Excel file: {str(e)}"}), 500

#     if 'text' not in new_reviews.columns:
#         return jsonify({"error": "The uploaded file must have a 'text' column"}), 400

#     if new_reviews['text'].isnull().any():
#         return jsonify({"error": "The 'text' column contains null values"}), 400

#     new_reviews['text'] = new_reviews['text'].apply(preprocess_text)
#     new_sequences = word_tokenizer.texts_to_sequences(new_reviews['text'])
#     new_padded = pad_sequences(new_sequences, padding='post', maxlen=max_len)

#     predictions = model.predict(new_padded)

#     # Chuyển đổi điểm thành nhãn cảm xúc
#     def get_sentiment_label(score):
#         if score > 0.6:
#             return "Positive"
#         elif score < 0.4:
#             return "Negative"
#         else:
#             return "Neutral"

#     new_reviews['sentiment'] = [
#         get_sentiment_label(score) for score in predictions.flatten()
#     ]

#     # Xuất file Excel với `openpyxl`
#     output_file = "predicted_sentiments.xlsx"
#     with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
#         new_reviews.to_excel(writer, index=False)

#     return send_file(output_file, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
### Backend: sentiment_analysis_api.py
# from flask import Flask, request, jsonify, send_file
# import pandas as pd
# import re
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import pickle

# app = Flask(__name__)

# # Load pre-trained model and tokenizer
# model = load_model("sentiment_model.h5")
# with open("tokenizer.pkl", "rb") as f:
#     word_tokenizer = pickle.load(f)

# vocab_size = 5000
# max_len = 100

# # Preprocessing function
# def preprocess_text(sen):
#     TAG_RE = re.compile(r'<[^>]+>')
#     sentence = TAG_RE.sub('', sen)
#     sentence = re.sub('[^a-zA-Z]', ' ', sentence)
#     sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
#     sentence = re.sub(r'\s+', ' ', sentence)
#     sentence = sentence.lower()
#     return sentence

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     if not file.filename.endswith('.xlsx'):
#         return jsonify({"error": "Invalid file format. Please upload an Excel file"}), 400

#     file.save("uploaded_file.xlsx")
#     return jsonify({"message": "File uploaded successfully"}), 200

# @app.route('/predict', methods=['POST'])
# def predict_sentiment():
#     try:
#         new_reviews = pd.read_excel("uploaded_file.xlsx")
#     except Exception as e:
#         return jsonify({"error": f"Error reading Excel file: {str(e)}"}), 500

#     if 'text' not in new_reviews.columns:
#         return jsonify({"error": "The uploaded file must have a 'text' column"}), 400

#     new_reviews['text'] = new_reviews['text'].apply(preprocess_text)
#     new_sequences = word_tokenizer.texts_to_sequences(new_reviews['text'])
#     new_padded = pad_sequences(new_sequences, padding='post', maxlen=max_len)

#     predictions = model.predict(new_padded)

#     def get_sentiment_label(score):
#         if score > 0.6:
#             return "Positive"
#         elif score < 0.4:
#             return "Negative"
#         else:
#             return "Neutral"

#     new_reviews['sentiment'] = [
#         get_sentiment_label(score) for score in predictions.flatten()
#     ]

#     output_file = "predicted_sentiments.xlsx"
#     with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
#         new_reviews.to_excel(writer, index=False)

#     return jsonify({"message": "Analysis complete. You can download the results."}), 200

# @app.route('/download', methods=['GET'])
# def download_file():
#     return send_file("predicted_sentiments.xlsx", as_attachment=True)

# @app.route('/dashboard', methods=['GET'])
# def dashboard():
#     data = pd.read_excel("predicted_sentiments.xlsx")
#     positive = data[data['sentiment'] == "Positive"].shape[0]
#     neutral = data[data['sentiment'] == "Neutral"].shape[0]
#     negative = data[data['sentiment'] == "Negative"].shape[0]

#     return jsonify({
#         "positive": positive,
#         "neutral": neutral,
#         "negative": negative
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
### Backend: sentiment_analysis_api.py
# from flask import Flask, request, jsonify, send_file, render_template
# import pandas as pd
# import re
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# import pickle

# app = Flask(__name__, static_folder='static', template_folder='templates')

# # Load pre-trained model and tokenizer
# model = load_model("sentiment_model.h5")
# with open("tokenizer.pkl", "rb") as f:
#     word_tokenizer = pickle.load(f)

# vocab_size = 5000
# max_len = 100

# # Preprocessing function
# def preprocess_text(sen):
#     TAG_RE = re.compile(r'<[^>]+>')
#     sentence = TAG_RE.sub('', sen)
#     sentence = re.sub('[^a-zA-Z]', ' ', sentence)
#     sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
#     sentence = re.sub(r'\s+', ' ', sentence)
#     sentence = sentence.lower()
#     return sentence

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files['file']
#     if not file.filename.endswith('.xlsx'):
#         return jsonify({"error": "Invalid file format. Please upload an Excel file"}), 400

#     file.save("uploaded_file.xlsx")
#     return jsonify({"message": "File uploaded successfully"}), 200

# # @app.route('/predict', methods=['POST'])
# # def predict_sentiment():
# #     try:
# #         new_reviews = pd.read_excel("uploaded_file.xlsx")
# #     except Exception as e:
# #         return jsonify({"error": f"Error reading Excel file: {str(e)}"}), 500

# #     if 'text' not in new_reviews.columns:
# #         return jsonify({"error": "The uploaded file must have a 'text' column"}), 400

# #     new_reviews['text'] = new_reviews['text'].apply(preprocess_text)
# #     new_sequences = word_tokenizer.texts_to_sequences(new_reviews['text'])
# #     new_padded = pad_sequences(new_sequences, padding='post', maxlen=max_len)

# #     predictions = model.predict(new_padded)

# #     def get_sentiment_label(score):
# #         if score > 0.6:
# #             return "Positive"
# #         elif score < 0.4:
# #             return "Negative"
# #         else:
# #             return "Neutral"

# #     new_reviews['sentiment'] = [
# #         get_sentiment_label(score) for score in predictions.flatten()
# #     ]

# #     output_file = "predicted_sentiments.xlsx"
# #     with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
# #         new_reviews.to_excel(writer, index=False)

# #     return jsonify({"message": "Analysis complete. You can download the results."}), 200

# import os  # Import thêm để kiểm tra file tồn tại

# @app.route('/predict', methods=['POST'])
# def predict_sentiment():
#     # Kiểm tra tệp đã được tải lên chưa
#     if not os.path.exists("uploaded_file.xlsx"):
#         return jsonify({"error": "File not found. Please upload a file first."}), 400

#     try:
#         new_reviews = pd.read_excel("uploaded_file.xlsx")
#     except Exception as e:
#         return jsonify({"error": f"Error reading Excel file: {str(e)}"}), 500

#     if 'text' not in new_reviews.columns:
#         return jsonify({"error": "The uploaded file must have a 'text' column"}), 400

#     new_reviews['text'] = new_reviews['text'].apply(preprocess_text)
#     new_sequences = word_tokenizer.texts_to_sequences(new_reviews['text'])
#     new_padded = pad_sequences(new_sequences, padding='post', maxlen=max_len)

#     predictions = model.predict(new_padded)

#     def get_sentiment_label(score):
#         if score > 0.6:
#             return "Positive"
#         elif score < 0.4:
#             return "Negative"
#         else:
#             return "Neutral"

#     new_reviews['sentiment'] = [
#         get_sentiment_label(score) for score in predictions.flatten()
#     ]

#     output_file = "predicted_sentiments.xlsx"
#     with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
#         new_reviews.to_excel(writer, index=False)

#     return jsonify({"message": "Analysis complete. You can download the results."}), 200

# @app.route('/download', methods=['GET'])
# def download_file():
#     return send_file("predicted_sentiments.xlsx", as_attachment=True)

# @app.route('/dashboard', methods=['GET'])
# def dashboard():
#     data = pd.read_excel("predicted_sentiments.xlsx")
#     positive = data[data['sentiment'] == "Positive"].shape[0]
#     neutral = data[data['sentiment'] == "Neutral"].shape[0]
#     negative = data[data['sentiment'] == "Negative"].shape[0]

#     return jsonify({
#         "positive": positive,
#         "neutral": neutral,
#         "negative": negative
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
### Backend: sentiment_analysis_api.py
from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import re
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load pre-trained model and tokenizer
model = load_model("sentiment_model.h5")
with open("tokenizer.pkl", "rb") as f:
    word_tokenizer = pickle.load(f)

vocab_size = 5000
max_len = 100

# Preprocessing function
def preprocess_text(sen):
    TAG_RE = re.compile(r'<[^>]+>')
    sentence = TAG_RE.sub('', sen)
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
    sentence = re.sub(r'\s+', ' ', sentence)
    sentence = sentence.lower()
    return sentence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if not file.filename.endswith('.xlsx'):
        return jsonify({"error": "Invalid file format. Please upload an Excel file"}), 400

    file.save("uploaded_file.xlsx")
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/predict', methods=['POST'])
def predict_sentiment():
    if not os.path.exists("uploaded_file.xlsx"):
        return jsonify({"error": "File not found. Please upload a file first."}), 400

    try:
        new_reviews = pd.read_excel("uploaded_file.xlsx")
    except Exception as e:
        return jsonify({"error": f"Error reading Excel file: {str(e)}"}), 500

    if 'text' not in new_reviews.columns:
        return jsonify({"error": "The uploaded file must have a 'text' column"}), 400

    new_reviews['text'] = new_reviews['text'].apply(preprocess_text)
    new_sequences = word_tokenizer.texts_to_sequences(new_reviews['text'])
    new_padded = pad_sequences(new_sequences, padding='post', maxlen=max_len)

    predictions = model.predict(new_padded)

    def get_sentiment_label(score):
        if score > 0.6:
            return "Positive"
        elif score < 0.4:
            return "Negative"
        else:
            return "Neutral"

    new_reviews['sentiment'] = [
        get_sentiment_label(score) for score in predictions.flatten()
    ]

    output_file = "predicted_sentiments.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        new_reviews.to_excel(writer, index=False)

    return jsonify({"message": "Analysis complete. You can download the results."}), 200

@app.route('/download', methods=['GET'])
def download_file():
    if not os.path.exists("predicted_sentiments.xlsx"):
        return jsonify({"error": "No analysis results found. Please perform an analysis first."}), 400

    return send_file("predicted_sentiments.xlsx", as_attachment=True)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if not os.path.exists("predicted_sentiments.xlsx"):
        return jsonify({"error": "No analysis results found. Please perform an analysis first."}), 400

    data = pd.read_excel("predicted_sentiments.xlsx")
    positive = data[data['sentiment'] == "Positive"].shape[0]
    neutral = data[data['sentiment'] == "Neutral"].shape[0]
    negative = data[data['sentiment'] == "Negative"].shape[0]

    return render_template('dashboard.html', positive=positive, neutral=neutral, negative=negative)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
