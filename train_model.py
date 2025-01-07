import pandas as pd
import re
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, LSTM, Dense
from sklearn.model_selection import train_test_split

# Load training dataset
try:
    movie_reviews = pd.read_csv("a1_IMDB_Dataset.csv")
except FileNotFoundError:
    print("Error: Training dataset file not found. Please check the path and try again.")
    exit()

# Preprocess text function
def preprocess_text(sen):
    TAG_RE = re.compile(r'<[^>]+>')
    sentence = TAG_RE.sub('', sen)
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
    sentence = re.sub(r'\s+', ' ', sentence)
    sentence = sentence.lower()
    stop_words = set(stopwords.words('english'))
    sentence = ' '.join(word for word in sentence.split() if word not in stop_words)
    return sentence

# Preprocess the text column
movie_reviews['review'] = movie_reviews['review'].apply(preprocess_text)

# Convert sentiment labels to binary (0 and 1)
movie_reviews['sentiment'] = movie_reviews['sentiment'].apply(lambda x: 1 if x == "positive" else 0)

# Prepare data for the model
X = movie_reviews['review']
y = movie_reviews['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tokenize and pad sequences
vocab_size = 5000
max_len = 100
word_tokenizer = Tokenizer(num_words=vocab_size)
word_tokenizer.fit_on_texts(X_train)
X_train = word_tokenizer.texts_to_sequences(X_train)
X_test = word_tokenizer.texts_to_sequences(X_test)
X_train = pad_sequences(X_train, padding='post', maxlen=max_len)
X_test = pad_sequences(X_test, padding='post', maxlen=max_len)

# Build and train the model
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=128, input_length=max_len),
    Conv1D(filters=64, kernel_size=3, activation='relu'),
    LSTM(64, return_sequences=True),
    GlobalMaxPooling1D(),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=5, batch_size=32, validation_split=0.2)

# Save the model and tokenizer
model.save("sentiment_model.h5")
import pickle
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(word_tokenizer, f)

print("Model and tokenizer saved successfully.")
