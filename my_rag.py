import sys
sys.path.append('/Users/clb/Desktop/project/code/paper/utils')
from call_openai import call_openai_embedding
from sklearn.metrics.pairwise import cosine_similarity

def get_corase_sift_res(claim, sentences, top_k=10):
    arr = [claim]
    arr.extend(sentences)
    embeddings = call_openai_embedding(arr)
    cosine_similarities = cosine_similarity(embeddings[0:1], embeddings[1:]).flatten()
    top_indices = cosine_similarities.argsort()[-min(top_k, len(cosine_similarities)):][::-1]
    corase_sift_res = [sentences[i] for i in top_indices]
    return corase_sift_res
