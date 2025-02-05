from utils.mistral_api import get_embeddings
import os
from pinecone import Pinecone, ServerlessSpec
from utils.test import load_json_anime

def split_into_chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# Initialize Pinecone client
pc = Pinecone(api_key='pcsk_2PdNQU_LF4psBHRnLPHMCcda8uoUTZejRHxVQVPuykXVR46MMVZvmbiD3Gh7bm6rusovHW')

# Create or connect to an index
index_name = "anime-cleaned"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1024,  # Adjust based on your embedding dimension (e.g., 384 for all-MiniLM-L6-v2)
        metric="cosine",  # Use "cosine" for cosine similarity
        spec=ServerlessSpec(
            cloud="aws",  # Choose your cloud provider
            region="us-east-1"  # Choose your region
        )
    )

# Connect to the index
index = pc.Index(index_name)

global_counter = 0
# Example data: list of anime titles and their embeddings

anime_json = load_json_anime()
anime_to_embed = [anime['description'] + anime['genre'] for anime in anime_json]
chunks_embedded = split_into_chunks(anime_to_embed, 100)
chunks_anime = split_into_chunks(anime_json, 100)

for chunk_a, chunk_e in zip(chunks_anime, chunks_embedded):

    anime_embeddings = get_embeddings(
        chunk_e
    ) 

    # Upsert embeddings with metadata
    vectors = []
    for i, (anime_metadata, embedding) in enumerate(zip(chunk_a, anime_embeddings)):
        unique_id = f"anime_{global_counter + i}"
        vectors.append((unique_id, embedding.embedding, {"anime": anime_metadata['name']}))
    # Upsert into Pinecone
    index.upsert(vectors=vectors)
    global_counter += len(chunk_a)
