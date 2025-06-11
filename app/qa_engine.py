import boto3
import json
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from app.config import (
    INDEX_PATH,
    DOCS_PATH,
    AWS_REGION,
    SAGEMAKER_ENDPOINT_NAME,
    EMBEDDING_MODEL
)

# Initialize session and client with correct profile
sagemaker_runtime = boto3.client(service_name ="sagemaker-runtime", region_name=AWS_REGION)

# Load embedding model
embedder = SentenceTransformer(EMBEDDING_MODEL)


def get_context(question, k=3):
    with open(DOCS_PATH, "rb") as f:
        docs = pickle.load(f)
    index = faiss.read_index(INDEX_PATH)
    q_vector = embedder.encode([question])
    _, I = index.search(q_vector, k)
    return "\n\n".join([docs[i] for i in I[0]])

def answer_question(question):
    context = get_context(question)

    prompt = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Answer the user's question using only the provided context. "
                "Do not restate or explain the question. Only output the final answer."
            )
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }
    ]

    try:
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT_NAME,
            ContentType="application/json",
            Body=json.dumps({
                "messages": prompt,
                "parameters": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "max_tokens": 128
                }
            }),
        )

        raw_output = response["Body"].read().decode()
        result = json.loads(raw_output)

        # Extract assistant's final message content
        output_text = None
        if "choices" in result and isinstance(result["choices"], list):
            output_text = result["choices"][0]["message"].get("content")

        if not output_text:
            return "No answer returned."

        # Optional: Extract answer part if "Answer:" marker exists
        if "**Answer:**" in output_text:
            return output_text.split("**Answer:**")[-1].strip()

        return output_text.strip()

    except Exception as e:
        return f"Error calling SageMaker endpoint: {str(e)}"
