# RAG Guardrail System

**AI Customer Support Validator for RAG-based Assistants**

---

# 1. Overview

This project implements a **RAG Guardrail Validation System** designed for enterprise customer support assistants. The goal is **not to generate answers**, but to **validate whether a Large Language Model (LLM) response is grounded in the company documentation**.

The system prevents hallucinations by verifying:

* The **user query matches documentation context**
* The **LLM response matches the retrieved documentation**
* The **LLM response answers the user query**

If the answer is unrelated or hallucinated, the system returns:

```
STOP_SESSION
```

instead of allowing the incorrect response to reach the user.

---

# 2. System Goals

This validator is designed to work alongside an existing **LLM support assistant** such as **Qwen, GPT, or any enterprise model**.

The system ensures:

* No hallucinated answers
* Answers grounded in company documentation
* Context relevance validation
* Automatic rejection of unrelated answers
* Lightweight validation using ML + semantic similarity

---

# 3. Architecture Overview

The system follows a **RAG + ML Guardrail architecture**.

```
User Query
      ↓
Retriever (FAISS Vector Search)
      ↓
Documentation Context
      ↓
Guardrail Validation (Query vs Context)
      ↓
LLM Generation (Qwen or other model)
      ↓
Guardrail Validation (Query + Context + Answer)
      ↓
ACCEPT or STOP_SESSION
```

The system **does not generate answers itself**.
It only validates responses produced by the external LLM.

---

# 4. Folder Structure

```
rag_guardrail_system
│
├── data
│   └── docs
│       ├── documentation files (.txt / .docx / .pdf)
│
├── models
│   ├── guardrail_classifier.pkl
│   ├── vector_index.faiss
│   └── chunks.pkl
│
├── src
│   ├── auto_data_generator.py
│   ├── auto_evaluator.py
│   ├── classifier_model.py
│   ├── config.py
│   ├── decision_engine.py
│   ├── document_loader.py
│   ├── feature_extractor.py
│   ├── main.py
│   ├── rag_model.py
│   ├── retriever.py
│   ├── train_classifier.py
│   └── vector_store.py
│
├── tests
│   └── test_queries.json
│
├── requirements.txt
└── README.md
```

---

# 5. Component Explanation

## data/docs

Contains company documentation such as:

* troubleshooting guides
* support instructions
* knowledge base articles

Supported formats:

```
.txt
.docx
.pdf
```

These documents form the **knowledge base**.

---

## models

Stores trained models and vector indexes.

```
guardrail_classifier.pkl
```

Machine learning model used to classify responses as:

```
ACCEPT
STOP_SESSION
```

```
vector_index.faiss
```

FAISS vector index containing document embeddings.

```
chunks.pkl
```

Stored document chunks corresponding to the vector embeddings.

---

# 6. Core System Components

## Document Loader

File:

```
src/document_loader.py
```

Responsibilities:

* Load documents from `data/docs`
* Extract text from PDF, DOCX, TXT
* Split documents into chunks

Example chunk:

```
Reset Password

1. Navigate to login page
2. Click "Forgot Password"
3. Enter your email
4. Follow reset link
```

---

## Vector Store

File:

```
src/vector_store.py
```

Responsibilities:

* Convert document chunks to embeddings
* Store embeddings in FAISS
* Perform similarity search

Embedding model used:

```
sentence-transformers/all-MiniLM-L6-v2
```

---

## Retriever

File:

```
src/retriever.py
```

Retrieves relevant documentation chunks.

Example query:

```
reset password
```

Retrieved context:

```
Reset Password Steps
1. Click forgot password
2. Enter registered email
3. Follow reset link
```

---

## Feature Extractor

File:

```
src/feature_extractor.py
```

Extracts validation features.

The system computes **four features**:

```
query_context_similarity
answer_context_similarity
query_answer_similarity
query_length
```

These are computed using cosine similarity.

Example:

```
[0.62, 0.78, 0.55, 3]
```

---

## Guardrail Classifier

File:

```
src/classifier_model.py
```

Machine learning model used:

```
RandomForestClassifier
```

Input:

```
[query_context, answer_context, query_answer, query_length]
```

Output:

```
ACCEPT
STOP_SESSION
```

---

## Decision Engine

File:

```
src/decision_engine.py
```

Responsible for final validation decision.

Hybrid approach used:

```
Semantic Similarity
+
Machine Learning Classifier
```

Decision rules:

```
Strong similarity → ACCEPT
Short query with moderate similarity → ACCEPT
Classifier confidence high → ACCEPT
Otherwise → STOP_SESSION
```

---

# 7. Training the Guardrail Model

Run:

```
python src/train_classifier.py
```

Training pipeline:

```
Load documents
      ↓
Generate synthetic training queries
      ↓
Extract similarity features
      ↓
Train RandomForestClassifier
      ↓
Save model
```

Generated dataset size:

```
200+ samples
```

---

# 8. Evaluation

Run:

```
python src/auto_evaluator.py
```

Example evaluation:

```
Query: reset password
Expected: ACCEPT
Predicted: ACCEPT

Query: random nonsense
Expected: STOP_SESSION
Predicted: STOP_SESSION

Accuracy: 0.83
```

---

# 9. Integration with Qwen Model

Your superior's system likely uses **Qwen for response generation**.

This guardrail system integrates **after the LLM generates an answer**.

### Example integration flow

```
User Query
↓
Retriever → Context
↓
Qwen generates response
↓
Guardrail Validator
↓
Return ACCEPT or STOP_SESSION
```

---

## Example Integration Code

Example pseudocode:

```
query = "I want to reset my password"

context = retriever.retrieve(query)

llm_answer = qwen.generate(query, context)

validation = guardrail.decide(query, context, llm_answer)

if validation == "ACCEPT":
    return llm_answer
else:
    return "Unable to answer. Please contact support."
```

---

# 10. Example End-to-End Flow

User query:

```
"I want to reset my password"
```

---

### Step 1: Retrieval

Retriever finds documentation:

```
Password Reset Guide
1. Go to login page
2. Click forgot password
3. Enter email
4. Follow reset link
```

---

### Step 2: Pre-validation

Similarity:

```
query_context_similarity = 0.65
```

Decision:

```
ACCEPT
```

---

### Step 3: LLM Generation (Qwen)

Qwen response:

```
1. Go to the login page
2. Click "Forgot Password"
3. Enter your registered email
4. Follow the reset link sent to your email
```

---

### Step 4: Response Validation

Computed features:

```
query_context = 0.65
answer_context = 0.71
query_answer = 0.60
```

Classifier result:

```
ACCEPT
```

Final output returned to user.

---

# 11. Example of Hallucination Detection

Query:

```
Git not working
```

Context:

```
Git troubleshooting guide
```

LLM hallucinated answer:

```
Reset Windows administrator password
```

Similarity:

```
answer_context_similarity = 0.05
```

Decision:

```
STOP_SESSION
```

Response is blocked.

---

# 12. Running the System

Train model:

```
python src/train_classifier.py
```

Run validator:

```
python src/main.py
```

Evaluate performance:

```
python src/auto_evaluator.py
```

---

# 13. Converting to Executable

To build executable:

```
pyinstaller --onefile --name rag_guardrail --add-data "data;data" --add-data "models;models" src/main.py
```

Output:

```
dist/rag_guardrail.exe
```

---

# 14. Dependencies

Install required packages:

```
pip install -r requirements.txt
```

Main libraries:

```
sentence-transformers
faiss-cpu
scikit-learn
numpy
python-docx
pdfplumber
torch
```

---

# 15. Future Improvements

Possible enhancements:

* Hybrid retrieval (BM25 + embeddings)
* Larger training dataset
* Context reranking
* Multi-turn conversation memory
* Stronger hallucination detection

---

# 16. Summary

This system acts as a **lightweight validation layer for enterprise LLM support assistants**.

It ensures that:

```
LLM responses stay grounded in documentation
Hallucinations are blocked
Users receive reliable troubleshooting instructions
```

The system integrates easily with models such as:

```
Qwen
Llama
```

making it suitable for production RAG pipelines.

---
