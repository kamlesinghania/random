import os
import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

language_key = os.environ.get('LANGUAGE_KEY')
language_endpoint = os.environ.get('LANGUAGE_ENDPOINT')

# Authenticate the client using your key and endpoint 
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

# Function to split text into chunks
def split_text(text, chunk_size=5120):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Function to categorize sentiment
#def categorize_sentiment(scores):
    # ... (same as before)

# Function to process sentiment analysis results
def process_results(documents, doc_result, original_docs):
    results = {}
    for document, analysis in zip(documents, doc_result):
        original_doc = original_docs[document]
        if original_doc not in results:
            results[original_doc] = {'positive': 0, 'neutral': 0, 'negative': 0, 'count': 0}
        
        results[original_doc]['positive'] += analysis.confidence_scores.positive
        results[original_doc]['neutral'] += analysis.confidence_scores.neutral
        results[original_doc]['negative'] += analysis.confidence_scores.negative
        results[original_doc]['count'] += 1

    # Calculate average scores and categorize sentiment
    for doc, scores in results.items():
        avg_scores = {k: v / scores['count'] for k, v in scores.items() if k != 'count'}
        #sentiment_category = categorize_sentiment(avg_scores)
        results[doc] = {
            'Text': doc,
            'Overall Positive': avg_scores['positive'],
            'Overall Neutral': avg_scores['neutral'],
            'Overall Negative': avg_scores['negative'],
            #'Sentiment Category': sentiment_category
        }

    return list(results.values())

# Method for detecting sentiment and opinions in text 
def sentiment_analysis_with_opinion_mining_example(client, documents_list):
    all_results = []
    batch = []
    original_docs = {}  # Map chunks to original documents

    for document in documents_list:
        if len(document) > 5120:
            chunks = split_text(document)
            for chunk in chunks:
                original_docs[chunk] = document
            batch.extend(chunks)
        else:
            original_docs[document] = document
            batch.append(document)

        # Process each batch
        if len(batch) >= 10:  # Assuming a batch size of 10, adjust as needed
            result = client.analyze_sentiment(batch, show_opinion_mining=True)
            all_results.extend(process_results(batch, result, original_docs))
            batch = []
            original_docs = {}

    # Process any remaining documents
    if batch:
        result = client.analyze_sentiment(batch, show_opinion_mining=True)
        all_results.extend(process_results(batch, result, original_docs))

    return pd.DataFrame(all_results)

# Example usage
documents_list = [
    "Your first text here, which can be up to 6000 characters or more.",
    "Your second text here, which can also be very long.",
     "The food and service were unacceptable. The concierge was nice, however."
]
df = sentiment_analysis_with_opinion_mining_example(client, documents_list)
print(df)

