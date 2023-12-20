from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import os
import pickle
from dotenv import dotenv_values
import tiktoken
import hashlib
config=dotenv_values(".env")
encoding = tiktoken.get_encoding("cl100k_base")
embeddings = OpenAIEmbeddings(openai_api_key=config["key"])

def num_tokens(docs):
    tokens = 0
    for doc in docs:
        t = len(encoding.encode(docs[0].page_content))
        tokens += t
    return tokens


def calc_embeddings(file_path):
    
    if os.path.exists("faiss_index"):
        db = FAISS.load_local("faiss_index", embeddings)
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        loader = PyPDFLoader(file_path)
        docs = loader.load_and_split(text_splitter)
        total_tokens = num_tokens(docs)
        cost=total_tokens/1000 * 0.000151
        db_new = FAISS.from_documents(documents=docs, embedding=embeddings)
        if not os.path.exists("faiss_index_individual"):
            os.makedirs("faiss_index_individual")
        db_new.save_local("faiss_index_individual/"+file_path.split('/')[-1])
        db.merge_from(db_new)
        db.save_local("faiss_index")
    else:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        
        loader = PyPDFLoader('/Users/anjugahlot/Downloads/Graduate Business Analyst_PD.pdf')
        docs = loader.load_and_split(text_splitter)
        total_tokens = num_tokens(docs)
        cost=total_tokens/1000 * 0.000151
        db = FAISS.from_documents(documents=docs, embedding=embeddings)
        db.save_local("faiss_index")
        db.save_local("faiss_index_individual/"+file_path.split('/')[-1])
    return(cost,total_tokens,db)
    


def create_embeddings(file_path):
    if os.path.exists("hashes.pkl"):
        with open('hashes.pkl', 'rb') as f:
            existing_hashes = pickle.load(f)
    else:   
        existing_hashes = set()


    def hash_file(file_path):
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def is_duplicate(content):
        content_hash = hash_file(content)
        if content_hash in existing_hashes:
            print( "File already exists in knowledge base")
            db = FAISS.load_local("faiss_index", embeddings)
            return (0,0,db)
        else:
            existing_hashes.add(content_hash)
            return calc_embeddings(file_path)
            # return False

    hash_file(file_path)
    x=is_duplicate(file_path)
    print(x)
    with open('hashes.pkl', 'wb') as f:
        pickle.dump(existing_hashes, f)
    return(x)
    

