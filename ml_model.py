import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

# Example of a content-based similarity check (could be based on actual ML model)
def compute_similarity(new_file_content, existing_file_contents):
    """ Compare file content using a basic string similarity algorithm (e.g., cosine similarity) """
    # Here we assume content is preprocessed and vectorized, like TF-IDF embeddings
    similarity_scores = []

    for content in existing_file_contents:
        # Convert contents to vectors (this is a placeholder; you'd use a real embedding in production)
        new_vector = np.array([ord(c) for c in new_file_content])  # Fake vectorization for demo
        existing_vector = np.array([ord(c) for c in content])  # Fake vectorization for demo

        similarity = cosine_similarity([new_vector], [existing_vector])[0][0]
        similarity_scores.append(similarity)

    return max(similarity_scores)

def detect_anomaly(features):
    """ A basic anomaly detection based on file size and timestamp (hour of day) """
    # In practice, you'd use a trained model or a statistical method
    size, hour = features
    # Example condition: anomaly if file size is too large or uploaded at unusual hours
    if size > 10 * 1024 * 1024 or (hour < 6 or hour > 23):  # File too large or night time
        return True
    return False
