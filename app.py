import tkinter
from tkinter.filedialog import askopenfilename
import os
from termcolor import colored
import time
import shutil
from emb import create_embeddings
from langchain.callbacks import get_openai_callback

from dotenv import dotenv_values
config=dotenv_values(".env")
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(openai_api_key=config["key"])
# turn on for windows
# os.system('color')


########################## LLM  ##########################################

from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
llm=ChatOpenAI(
    temperature=0.1, model_name="gpt-3.5-turbo",openai_api_key=config["key"]
)

# Adapt if needed
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:""")



############################################################################################################



print (colored(">>>Hello! I'm your assistant ready to help with your queries.", 'green'))

def loading_animation(duration=3):
    print("Loading", end="")
    for _ in range(duration):
        for char in ['.', '..', '...', '......']:
            print(char, end="\r")
            time.sleep(0.1)
            print("       ", end="\r")  

def list_and_select_file():
    uploads_dir = os.path.join(os.getcwd(), 'uploads')

    # Check if the uploads directory exists
    if not os.path.exists(uploads_dir):
        print("No uploads directory found.")
        return None

    # List all files in the uploads directory
    files = [f for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
    
    if not files:
        print("No files found in the uploads directory.")
        return None

    # Print the list of files with numbers
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    # Ask the user to select a file
    try:
        choice = int(input("Select a file number: "))
        if 1 <= choice <= len(files):
            selected_file = files[choice - 1]
            return os.path.join(uploads_dir, selected_file)
        else:
            print("Invalid selection. Please enter a number from the list.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def main_menu():
    loading_animation()  

    while True:
        print(colored("\nPlease choose an option:", "green"))
        print(colored("1. Add files to Knowledge base", "green"))
        print(colored("2. Query particular file", "green"))
        print(colored("3. Query whole knowledge base", "green"))
        print(colored("4. Exit", "green"))

        try:
            choice = int(input(colored("Enter your choice (1-4): ", "blue")))

            if choice == 1:
                print(colored("Option 1 selected: Add files to Knowledge base", "blue"))
                print(colored("Please select the file you want to add to the knowledge base", "green"))
                tkinter.Tk().withdraw()
                filename = askopenfilename()
                uploads_dir = os.path.join(os.getcwd(), 'uploads')
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)
                destination_file_path = os.path.join(uploads_dir, os.path.basename(filename))
                shutil.copy(filename, destination_file_path)
                print(colored("File added to knowledge base", "green"))
                create_embeddings(destination_file_path)
                print(colored("...............................................", "green"))


            elif choice == 2:
                print(colored("Option 2 selected: Query particular file", "blue"))
                selected_file_path = list_and_select_file()
                if selected_file_path:
                    n=selected_file_path.split('/')[-1]
                    print(colored(f"Ask me anything from {n}", "green"))
                # x=create_embeddings(selected_file_path)
                
                    db = FAISS.load_local("faiss_index_individual/"+n, embeddings)
                    while True:
                        query = input(colored("Enter your query: ", "blue"))
                        if query == "exit":
                            break
                        else:
                            # print(db.similarity_search(query)[0].page_content)
                            qa = ConversationalRetrievalChain.from_llm(llm=llm,
                                           retriever=db.as_retriever(),
                                           condense_question_prompt=CONDENSE_QUESTION_PROMPT,
                                           return_source_documents=True,
                                           verbose=False)
                            chat_history = []
                            result = qa({"question": query, "chat_history": chat_history})
                            print(result["answer"])

                else:
                    print(colored("No files found in the uploads directory.", "red"))



            elif choice == 3:
                print(colored("Option 3 selected: Query whole knowledge base", "blue"))
                db = FAISS.load_local("faiss_index", embeddings)
                while True:
                    query = input(colored("Enter your query: ", "blue"))
                    if query == "exit":
                        break
                    else:
                        # print(db.similarity_search(query)[0].page_content)
                        qa = ConversationalRetrievalChain.from_llm(llm=llm,
                                        retriever=db.as_retriever(),
                                        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
                                        return_source_documents=True,
                                        verbose=False)
                        chat_history = []
                        result = qa({"question": query, "chat_history": chat_history})
                        print(result["answer"])

                # Implement the logic for querying the whole knowledge base
            elif choice == 4:
                print(colored("Exiting...", "blue"))
                break
            else:
                print(colored("Invalid choice, please try again.", "red"))
        except ValueError:
            print(colored("Invalid input, please enter a number from 1 to 4.", "red"))

with get_openai_callback() as cb:
    main_menu()
    print(cb)




