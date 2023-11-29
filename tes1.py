from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Function to perform lemmatization
def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    word_list = word_tokenize(text)
    lemmatized_output = ' '.join([lemmatizer.lemmatize(w) for w in word_list])
    return lemmatized_output

# Modify the sentiment_analysis_with_opinion_mining_example function
def sentiment_analysis_with_opinion_mining_example(client, documents_list):
    all_results = []
    batch = []
    original_docs = {}  # Map chunks to original documents

    for document in documents_list:
        # Apply lemmatization
        document = lemmatize_text(document)

        if len(document) > 5120:
            chunks = split_text(document)
            for chunk in chunks:
                original_docs[chunk] = document
            batch.extend(chunks)
        else:
            original_docs[document] = document
            batch.append(document)

        # ... (rest of the function remains the same)

# ... (rest of your existing code)

