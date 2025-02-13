from dotenv import load_dotenv
load_dotenv(override=True)
import os
from typing import List
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain.schema import Document
from sklearn.feature_extraction.text import TfidfVectorizer

from langchain_core.tools import tool
# import nltk
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger_eng')

# from langchain_community.document_loaders import UnstructuredMarkdownLoader
# from langchain_text_splitters import MarkdownHeaderTextSplitter


class MarkdownVectorDB:
    def __init__(
        self, persist_directory: str = "./dump/vector_store_data", markdown_folder: str = "markdown_data"
    ):
        self.persist_directory = persist_directory
        self.markdown_folder = markdown_folder
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=700, chunk_overlap=150
        )
        self.vector_store = None

    def _initialize_vector_store(self):
        """Initializes the vector store using Chroma."""
        return Chroma(
            embedding_function=self.embeddings, persist_directory=self.persist_directory
        )

    def process_markdown_files(self):
        """Processes markdown files into document chunks."""
        documents = []

        for filename in os.listdir(self.markdown_folder):
            if filename.endswith(".md"):
                filepath = os.path.join(self.markdown_folder, filename)

                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    chunks = self.text_splitter.split_text(content)

                    for chunk in chunks:
                        keywords = self.extract_keywords(chunk)
                        doc = Document(
                            page_content=chunk,
                            metadata={
                                "filename": filename,
                                "keywords": ",".join(keywords),
                            },
                        )
                        documents.append(doc)

        return documents

    def generate_vector_database(self):
        """Generates the vector database by processing documents and adding them to Chroma."""
        documents = self.process_markdown_files()
        self.vector_store = self._initialize_vector_store()
        self.vector_store.add_documents(documents)
        self.vector_store.persist()
        print(f"Processed and added {len(documents)} chunks to the vector database.")

    def load_vector_database(self):
        """Loads the existing vector database from the persistence directory."""
        print("Loading existing vector database...")
        self.vector_store = self._initialize_vector_store()
        print(f"Loaded vector database.")

    def retrieve_documents(self, query: str, top_k: int = 5) -> List[Document]:
        """Retrieves the top-k documents similar to the query."""
        if self.vector_store is None:
            raise ValueError(
                "Vector store is not initialized. Load or generate the vector store first."
            )

        print("Retrieving documents...")
        results = self.vector_store.similarity_search(query, k=top_k)
        return results

    @staticmethod
    def extract_keywords(chunk: str, top_n: int = 10) -> List[str]:
        """Extracts keywords from a text chunk using TF-IDF."""
        documents = [chunk]
        tfidf_vectorizer = TfidfVectorizer(stop_words="english", max_features=top_n)
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
        feature_array = np.array(tfidf_vectorizer.get_feature_names_out())
        tfidf_sorting = np.argsort(tfidf_matrix.toarray()).flatten()[::-1]
        top_keywords = feature_array[tfidf_sorting][:top_n]
        return top_keywords.tolist()

    def recreate_or_load_vector_db(self, recreate: bool = False):
        """Recreates or loads the vector database based on the input flag."""
        if not os.path.exists(self.persist_directory) or recreate:
            os.makedirs(self.persist_directory, exist_ok=True)
            print("Recreating vector database...")
            self.generate_vector_database()
        else:
            print("Loading vector database...")
            self.load_vector_database()

# Example Usage
vector_db = MarkdownVectorDB()
vector_db.recreate_or_load_vector_db(recreate=False)
retriever = vector_db.vector_store.as_retriever()

@tool
def lookup_policy(query: str) -> str:
    """Consults the company policies to check whether certain options are permitted.
    Know more about the policies, guidelines, and procedures or any other FAQs of the company."""
    try:
        docs = vector_db.retrieve_documents(query, top_k=2)
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error during lookup: {str(e)}"