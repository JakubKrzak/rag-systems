from pathlib import Path
import chromadb
from openai import OpenAI

#configuration
CHROMA_DIR = Path("/home/kuba/rag-systems/data/chroma")
COLLECTION_NAME = "transformers_papers"
EMBEDDING_MODEL = "text-embedding-3-small"
LLM = "gpt-4o-mini"
TOP_K = 6
MAX_CONTEX_CHARS = 12000

client = OpenAI()

chroma = chromadb.PersistentClient(path=CHROMA_DIR)
collection = chroma.get_collection(name=COLLECTION_NAME)

#Embedding query
def embed_query(text: str) -> list[float]:
    """Change text into embedding 
        vector using OpenAI model"""
    
    res_emb_query = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return res_emb_query.data[0].embedding



#retrival
def retrival(question: str, k: int = TOP_K) -> dict:
    """Returning k most similar documents from Chroma index
        based on question embedding
        documents, metadatas and distances"""
    
    q_emb = embed_query(question)

    res_retrival = collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    return res_retrival



def context(response):
    
    docs = response["documents"][0]
    metas = response["metadatas"][0]

    parts = []
    cities = []
    total = 0

    for i in range(len(docs)):
        doc = docs[i]
        meta = metas[i]

        paper_id = meta["paper_id"]
        chunk_id = meta["chunk_id"]

        cite = f"[paper_id:{paper_id}, chunk_id:{chunk_id}]"
        piece = cite + "\n" + doc

        parts.append(piece)
        cities.append(cite)
    
    context_text = "\n\n---\n\n".join(parts)
    return context_text, cities




def ask_llm(question, contex_text):
    responseLLM = client.chat.completions.create(
        model=LLM,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": "Answer only based on the provided context. If the information is not in the context, respond: I don't know."
            },
            {
                "role": "user",
                "content": "Question:\n" + question + "\n\Kontekst:\n" + contex_text
            }
        ]
    )
    anserw = responseLLM.choices[0].message.content
    return anserw

def rag_step(question):
    response = retrival(question, TOP_K)
    context_text, cities = context(response)
    anserw = ask_llm(question, context_text)
    return anserw, cities

#user
print("Zadaj pytanie")
question_user = input()


anserw, cities = rag_step(question_user)

print("\nOdpowiedz:")
print(anserw)

print("m\Cyrowania:")
print(" ".join(cities))