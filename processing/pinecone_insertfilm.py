import json
from mistral_api import get_embeddings
from pinecone import Pinecone, ServerlessSpec

def load_json_films():
    """Load film data from the 3film.json file."""
    with open('3.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def create_film_text(film):
    """Create a combined text representation of the film for embedding."""
    return f"{film['description']} {film['genre']} {film['title']}"

def split_into_chunks(lst, n):
    """Split a list into chunks of size n."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def initialize_pinecone(api_key, index_name="film-embed"):
    """Initialize Pinecone client and create index if it doesn't exist."""
    pc = Pinecone(api_key=api_key)
    
    # Create index if it doesn't exist
   
    index_name = "tv-series"
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1024,  # Adjust based on your embedding dimension (e.g., 384 for all-MiniLM-L6-v2)
            metric="cosine",
            spec=ServerlessSpec(
            cloud="aws",  # Choose your cloud provider
            region="us-east-1"  # Choose your region
        )  # Use "cosine" for cosine similarity
        )
    return pc.Index(index_name)

def insert_films_to_pinecone(api_key, batch_size=75):
    """Main function to process films and insert them into Pinecone."""
    # Load film data
    films = load_json_films()
    
    # Initialize Pinecone
    index = initialize_pinecone(api_key)
    
    # Prepare films for embedding
    films_to_embed = [create_film_text(film) for film in films]
    
    # Process in batches
    global_counter = 0
    for film_chunk, text_chunk in zip(
        split_into_chunks(films, batch_size),
        split_into_chunks(films_to_embed, batch_size)
    ):
        print(film_chunk, text_chunk)
        # Get embeddings for the chunk
        embeddings = get_embeddings(text_chunk)
        
        # Prepare vectors with metadata
        vectors = []
        for i, (film, embedding) in enumerate(zip(film_chunk, embeddings)):
            unique_id = f"film_{global_counter + i}"
            # Include all film metadata
            metadata = {
                "title": film["title"],
            }
            vectors.append((
                unique_id,
                embedding.embedding,
                metadata
            ))

        # Upsert batch into Pinecone
        print(vectors)
        index.upsert(vectors=vectors)
        global_counter += len(film_chunk)
        print(f"Inserted {global_counter} films into Pinecone")

if __name__ == "__main__":
    # Replace with your Pinecone API key
    PINECONE_API_KEY = ""
    
    try:
        insert_films_to_pinecone(PINECONE_API_KEY)
        print("Successfully completed inserting all films into Pinecone")
    except Exception as e:
        print(f"An error occurred: {str(e)}")