from fastapi import FastAPI, UploadFile, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import google.generativeai as genai
from pydantic import BaseModel

# Set the API key
os.environ['GEMINI_API_KEY'] = 'AIzaSyC7-yI_qVC8wBhB38hIKcleN5nUaza1bgA'
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Paths
UPLOAD_DIR = "uploads"
VECTOR_DB_PATH = "vectorstore/db_faiss"

# Create FastAPI app
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows requests from your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Vector Database Creation
def create_vector_db(file_paths):
    documents = []
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(VECTOR_DB_PATH)

# Endpoint: Upload PDFs and Create Vector Database
@app.post("/upload")
async def upload_pdfs(files: list[UploadFile]):
    if not all(file.filename.endswith(".pdf") for file in files):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_paths = []
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        file_paths.append(file_path)

    create_vector_db(file_paths)
    return {"message": "PDFs uploaded and vector database created successfully."}

# Pydantic model for the query
class QueryModel(BaseModel):
    query: str

# Endpoint: Ask a Question
@app.post("/ask")
async def ask_question(request: Request):
    if request.headers["Content-Type"] == "application/json":
        data = await request.json()
        query = data.get("query")
    else:
        form_data = await request.form()
        query = form_data.get("query")

    if not query:
        raise HTTPException(status_code=422, detail="Query is required.")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 2})
    docs = retriever.get_relevant_documents(query)

    context = "\n".join([doc.page_content for doc in docs])
    response = gemini_model.generate_content(
        f"Context: {context}\nQuestion: {query}\nAnswer only the question accurately:"
    )

    sources = [{"page": doc.metadata.get("page", "N/A"), "content": doc.page_content} for doc in docs]
    return JSONResponse({"answer": response.text, "sources": sources})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


