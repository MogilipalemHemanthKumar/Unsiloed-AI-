# Unsiloed-AI-Assignment

## Overview

This project is a full-stack application that allows users to upload PDF files, create a vector database from the uploaded PDFs, and interact with a chatbot to ask questions based on the content of the PDFs. The backend is built using FastAPI, and the frontend is built using React.

## Project Structure

```
Unsiloed-AI-Assignment/
├── app/
│   ├── main.py
│   ├── init.py
│   └── ...
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── ...
├── README.md
```

## Backend (FastAPI)

### Setup

1. **Navigate to the app directory**:
   ```bash
   cd Unsiloed-AI-Assignment/app
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   * On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   * On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Backend

Run the FastAPI application:
```bash
uvicorn main:app --reload
```

## Frontend (React)

### Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd Unsiloed-AI-Assignment/frontend
   ```

2. **Install the required dependencies**:
   ```bash
   npm install
   ```

### Running the Frontend

Start the React application:
```bash
npm start
```

## How It Works

* **Upload PDFs**: Users can upload one or more PDF files. The backend processes these PDFs, creates a vector database, and stores it locally.
* **Chat Interface**: Users can interact with a chatbot to ask questions based on the content of the uploaded PDFs. The chatbot uses the vector database to retrieve relevant information and generate answers.
* **Beautiful UI**: The chat interface is designed to be user-friendly and visually appealing, with spacing between consecutive questions and answers.

## Features

* **Multiple PDF Uploads**: Users can upload multiple PDFs at once.
* **Vector Database**: The backend creates a vector database from the uploaded PDFs for efficient information retrieval.
* **Chatbot**: Users can ask questions based on the content of the uploaded PDFs.
* **Beautiful UI**: The chat interface is designed to be user-friendly and visually appealing.


