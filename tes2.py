from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

def summarize_text(text, max_length=130, min_length=30):
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

# Modify the sentiment_analysis_with_opinion_mining_example function
def sentiment_analysis_with_opinion_mining_example(client, documents_list):
    all_results = []
    batch = []
    original_docs = {}  # Map chunks to original documents

    for document in documents_list:
        # Apply summarization
        summarized_document = summarize_text(document)

        if len(summarized_document) > 5120:
            chunks = split_text(summarized_document)
            for chunk in chunks:
                original_docs[chunk] = summarized_document
            batch.extend(chunks)
        else:
            original_docs[summarized_document] = summarized_document
            batch.append(summarized_document)

        # ... (rest of the function remains the same)

# ... (rest of your existing code)

