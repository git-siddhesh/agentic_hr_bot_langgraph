from langchain_core.tools import tool
import os 
# import nltk
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')

from dotenv import load_dotenv
load_dotenv(override=True)
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

# headers_to_split_on = [
#     ("#", "Header 1"),
#     ("##", "Header 2"),
#     ("###", "Header 3"),
#     ("####", "Header 4"),
#     ("#####", "Header 5"),
#     ("######", "Header 6"),
#     ("```", "Code Block"),
#     ("---", "Horizontal Rule"),
#     ("*", "List Item"),
#     ("1.", "List Item"),
#     ("-", "List Item"),
#     ("[", "Link"),
#     ("![", "Image"),
#     (">", "Block Quote"),
#     ("|", "Table"),
# ]





class MarkdownVectorDB:
    def __init__(
        self, persist_directory: str=".\\dump\\vector_store_data", markdown_folder: str="markdown_data"
    ):
        self.persist_directory = persist_directory
        self.markdown_folder = markdown_folder
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700, chunk_overlap=150
        )
        # self.markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)


        self.vector_store = None

    def _initialize_vector_store(self):

        return Chroma(
            embedding_function=self.embeddings, persist_directory=self.persist_directory
        )

    def process_markdown_files(self):
        documents = []

        for filename in os.listdir(self.markdown_folder):
            if filename.endswith(".md"):
                filepath = os.path.join(self.markdown_folder, filename)

                # loader = UnstructuredMarkdownLoader(filepath , mode="elements",  strategy="fast")
                # data = loader.load_and_split(text_splitter=self.text_splitter)
                
                # for chunk in data:
                #     print(chunk.page_content)
                #     input()
                #     keywords = self.extract_keywords(chunk.page_content)
                #     chunk.metadata["keywords"] = ",".join(keywords)
                #     documents.append(chunk)
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    chunks = self.text_splitter.split_text(content)
                    # chunks = self.markdown_splitter.split_text(content)
                   
                    for chunk in chunks:
                        keywords = self.extract_keywords(chunk)
                        doc = Document(page_content=chunk, metadata={
                            "filename": filename,
                            "keywords": ",".join(keywords)
                        })
                        
                        documents.append(doc)

        return documents

    def generate_vector_database(self):
        documents = self.process_markdown_files()
        self.vector_store = self._initialize_vector_store()
        self.vector_store.add_documents(documents)
        # self.vector_store.persist()
        print(f"Processed and added {len(documents)} chunks to the vector database.")

    def load_vector_database(self):
        print("Loading existing vector database...")
        self.vector_store = self._initialize_vector_store()

    def retrieve_documents(self, query: str, top_k: int = 5) -> List[Document]:
        if self.vector_store is None:
            raise ValueError(
                "Vector store is not initialized. Load or generate the vector store first."
            )
        print('&&&&&&&&&&&&&&&&&&&&&&')
        print("retrive documents invoked")
        results = self.vector_store.similarity_search(query, k=top_k)
        print("results", results)
        return results

    @staticmethod
    def extract_keywords(chunk: str, top_n: int = 10) -> List[str]:
        documents = [chunk]
        tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        feature_array = np.array(tfidf_vectorizer.get_feature_names_out())
        tfidf_sorting = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
        top_keywords = feature_array[tfidf_sorting][:top_n]
        return top_keywords.tolist()

    def recreate_or_load_vector_db(self, recreate:bool=False):
        if not os.path.exists(self.persist_directory) or recreate:
            os.makedirs(self.persist_directory, exist_ok=True)
            print("Recreating vector database...")
            self.generate_vector_database()
        else:
            print("Loading vector database...")
            self.load_vector_database()



vector_store = Chroma(embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"), 
                      persist_directory=".\\dump\\vector_store_data")

retriever = vector_store.as_retriever()




@tool 
def lookup_policy(query: str)-> str:
    """Consult the company policies to check whether certain options are permitted.
    Fetch the general policies and guidelines from the company's internal documents.
    """
    print("retrive documents invoked")

    docs = vector_store.similarity_search("leave policy", k=1)
    print("retrive documents completed")
    return "No policy found"


# @tool
# def lookup_policy(query: str) -> str:
#     """Consult the company policies to check whether certain options are permitted.
#     Fetch the general policies and guidelines from the company's internal documents.
    
#     Args: 
#         query: The query to search for in the company policies.

#     Returns:
#         str: The relevant company policies that match the query 
    
#     """
#     print('&&&&&&&&&&&&&&&&&&&&&&')
#     print("retrive documents invoked")
#     results = vector_store.simila   rity_search(query, k=5)
#     print("results", results)
#     return "\n\n".join([doc.page_content for doc in results])
