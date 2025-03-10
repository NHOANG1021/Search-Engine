import math
import heapq

def page_rank_tokens(url_word_freq):
    """Returns a dictionary of total number of tokens in each URL."""
    return {url: sum(posting[1] for posting in postings) for url, postings in url_word_freq.items()}

def page_rank_weights(url_word_freq, url_tokens):
    """Returns a list of the weights of each token in a URL."""
    return [[round(posting[1] / url_tokens[url], 2) for posting in postings] for url, postings in url_word_freq.items()]

def page_rank(url_word_freq, query, url_tokens):
    """Computes a score for each URL based on word weights and query relevance."""
    scores = {}
    weights = page_rank_weights(url_word_freq, url_tokens)

    for (url, words), weight_list in zip(url_word_freq.items(), weights):
        scores[url] = sum(freq * weight for (word, freq, _), weight in zip(words, weight_list) if word in query)

    return scores

def tf_idf(url_word_freq, query, num_docs=55393):
    """Computes TF-IDF scores for each URL based on query relevance."""
    return {
        url: sum((1 + math.log(tf_t_d)) * math.log(num_docs / df_t) for word, tf_t_d, df_t in words if word in query)
        for url, words in url_word_freq.items()
    }

def merge_scores(url_word_freq, query):
    """Merges PageRank and TF-IDF scores and returns the top 5 URLs."""
    url_tokens = page_rank_tokens(url_word_freq)
    pagerank_scores = page_rank(url_word_freq, query, url_tokens)
    tfidf_scores = tf_idf(url_word_freq, query)

    final_scores = {url: (tfidf_scores.get(url, 0) + pagerank_scores.get(url, 0)) / 2 for url in url_word_freq}

    top_5 = heapq.nlargest(5, final_scores.items(), key=lambda x: x[1])

    return top_5