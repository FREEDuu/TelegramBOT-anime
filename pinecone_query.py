from pinecone import Pinecone, ServerlessSpec
from mistral_api import get_embeddings

def make_query(pc,description, type):
    anime_embeddings = get_embeddings(
        [
            description
        ]
    )[0]
    # Create or connect to an index
    index_name = type #anime_cleaned
    index = pc.Index(index_name)


    # Query Pinecone for similar anime
    results = index.query(
        vector=anime_embeddings.embedding,
        top_k=30,  # Number of similar anime to retrieve
        include_metadata=True  # Include metadata in the response
    )

    # Display results with titles
    return results['matches']        
   