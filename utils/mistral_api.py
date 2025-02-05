import os
from mistralai import Mistral

def get_embeddings(anime_data):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-embed"

    client = Mistral(api_key=api_key)

    embeddings_batch_response = client.embeddings.create(
        model=model,
        inputs=anime_data,
    )
    return embeddings_batch_response.data

