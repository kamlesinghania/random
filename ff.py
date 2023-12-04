import os
import json
import logging
from datetime import datetime
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient, AnalyzeSentimentAction


key = os.environ.get('LANGUAGE_KEY')
endpoint = os.environ.get('LANGUAGE_ENDPOINT')

# Configure logging
logging.basicConfig(filename='sentiment_analysis.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

cost_per_1000_docs = 1.5057  # AUD

def calculate_cost(num_docs):
    return (num_docs / 1000) * cost_per_1000_docs

def count_documents(documents, max_chars_per_doc=1000):
    doc_count = 0
    for doc in documents:
        doc_count += -(-len(doc) // max_chars_per_doc)  # Ceiling division to count each 1000-character segment as a document
    return doc_count

# Function to convert the analysis result to a serializable format
def convert_to_json_serializable(document_results, documents):
    results_list = []
    for doc, doc_results in zip(documents, document_results):
        for result in doc_results:
            if not result.is_error:
                doc_dict = {
                    "document_text": doc,
                    "id": result.id,
                    "sentiment": result.sentiment,
                    "confidence_scores": {
                        "positive": result.confidence_scores.positive,
                        "neutral": result.confidence_scores.neutral,
                        "negative": result.confidence_scores.negative
                    },
                    "sentences": []
                }
                for sentence in result.sentences:
                    sentence_dict = {
                        "text": sentence.text,
                        "sentiment": sentence.sentiment,
                        "confidence_scores": {
                            "positive": sentence.confidence_scores.positive,
                            "neutral": sentence.confidence_scores.neutral,
                            "negative": sentence.confidence_scores.negative
                        },
                        "mined_opinions": []
                    }
                    for opinion in sentence.mined_opinions:
                        opinion_dict = {
                            "target": {
                                "text": opinion.target.text,
                                "sentiment": opinion.target.sentiment,
                                "confidence_scores": {
                                    "positive": opinion.target.confidence_scores.positive,
                                    "neutral": opinion.target.confidence_scores.neutral,
                                    "negative": opinion.target.confidence_scores.negative
                                }
                            },
                            "assessments": []
                        }
                        for assessment in opinion.assessments:
                            assessment_dict = {
                                "text": assessment.text,
                                "sentiment": assessment.sentiment,
                                "confidence_scores": {
                                    "positive": assessment.confidence_scores.positive,
                                    "neutral": assessment.confidence_scores.neutral,
                                    "negative": assessment.confidence_scores.negative
                                },
                                "is_negated": assessment.is_negated
                            }
                            opinion_dict["assessments"].append(assessment_dict)
                        sentence_dict["mined_opinions"].append(opinion_dict)
                    doc_dict["sentences"].append(sentence_dict)
                results_list.append(doc_dict)
            else:
                print(f"Document with ID {result.id} had an error: {result.error}")

    return results_list

# Function to create batches of documents and track included documents
def create_batches(documents, max_docs_per_batch, max_chars_per_doc):
    
    batches = []
    current_batch = []
    included_documents = []

    for doc in documents:
        if len(doc) <= max_chars_per_doc:
            if len(current_batch) < max_docs_per_batch:
                current_batch.append(doc)
                included_documents.append(doc)
            else:
                batches.append(current_batch)
                current_batch = [doc]
                included_documents = [doc]
        else:
            logging.warning(f"Document skipped (length {len(doc)} characters)")

    if current_batch:
        batches.append(current_batch)

    return batches, included_documents

# Azure credentials and client setup
key = os.environ.get('LANGUAGE_KEY')
endpoint = os.environ.get('LANGUAGE_ENDPOINT')
text_analytics_client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key),
)
# Documents for analysis
documents = [
    "The hotel was good but hygiene was bad",
    "The hotel was good but hygiene was bad and sad",
    "something very big"
]

# Create batches of documents and get the list of included documents
batches, included_documents = create_batches(documents, max_docs_per_batch=25, max_chars_per_doc=120000)

# Perform sentiment analysis on each batch
all_results = []
total_cost = 0
num_docs_for_pricing = 0
for batch in batches:
    num_docs_in_batch = count_documents(batch)
    num_docs_for_pricing+= num_docs_in_batch
    batch_cost = calculate_cost(num_docs_in_batch)
    total_cost += batch_cost

    logging.info(f"Sending {len(batch)} documents for analysis. Total documents (considering character limit): {num_docs_in_batch}. Estimated cost for this batch: ${batch_cost:.4f}")
    doc_lengths = [len(doc) for doc in batch]
    logging.info(f"Sending {len(batch)} documents for analysis. Lengths: {doc_lengths}")
    poller = text_analytics_client.begin_analyze_actions(
        batch,
        display_name="Batch Text Analysis",
        actions=[
            AnalyzeSentimentAction(show_opinion_mining=True),
        ],
    )
    document_results = poller.result()
    all_results.extend(document_results)
    logging.info('-' * 70)  # Print a line of dashes after each request

# Convert the results to a JSON serializable format
json_serializable_results = convert_to_json_serializable(all_results, included_documents)

# Save the results to a JSON file
with open('sentiment_analysis_results.json', 'w') as f:
    json.dump(json_serializable_results, f, indent=4)
logging.info(f"Total estimated cost for all batches: ${total_cost:.4f}")
logging.info(f"Total docs for pricing: {num_docs_for_pricing}")
logging.info("Sentiment analysis completed.")

print("Results saved to sentiment_analysis_results.json")
