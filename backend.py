# backend.py
import os
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class AgriBrain:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.vector_store = None
        self.model = genai.GenerativeModel('gemini-pro')
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self):
        # Load agricultural documents from docs directory
        docs = []
        for file in os.listdir("docs"):
            if file.endswith(".pdf"):
                loader = PyPDFLoader(f"docs/{file}")
                docs.extend(loader.load())
        
        if docs:
            chunks = self.text_splitter.split_documents(docs)
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)

    def get_response(self, query):
        if self.vector_store:
            similar_docs = self.vector_store.similarity_search(query, k=3)
            context = "\n".join([doc.page_content for doc in similar_docs])
        else:
            context = "General agricultural knowledge"
            
        prompt = f"""You are AgriBrain, an AI assistant for farmers. Use this context:
        {context}
        
        Answer the following question in simple, practical terms suitable for farmers:
        {query}
        
        Provide clear, actionable advice and consider local farming practices in India."""
        
        response = self.model.generate_content(prompt)
        return response.text

agribrain = AgriBrain()
try:
    import pwd
except ImportError:
    # Handle the case where pwd is not available (e.g., on Windows)
    class PwdDummy:
        def getpwuid(self, uid):
            return "dummy_user"
    pwd = PwdDummy()