import math

def page_rank_tokens(url_word_freq: dict) -> list:
    """
    Returns a list of total number of tokens in each URL.
    """
    return [(url, sum(posting[1] for posting in postings)) for url, postings in url_word_freq.items()]

def page_rank_weights(url_word_freq: dict) -> list:
    """
    Returns a list of the weights of each token in a URL.
    """
    url_tokens = {url: total for url, total in page_rank_tokens(url_word_freq)}
    return [[round(posting[1] / url_tokens[url], 2) for posting in postings] for url, postings in url_word_freq.items()]

def page_rank(url_word_freq: dict, query: list) -> dict:
    """
    Computes a score for each URL based on word weights and query relevance.
    """
    scores = {}
    weights = page_rank_weights(url_word_freq)

    for (url, words), weight_list in zip(url_word_freq.items(), weights):
        scores[url] = sum(freq * weight for (word, freq, _), weight in zip(words, weight_list) if word in query)

    return scores

def tf_idf(url_word_freq: dict, query: list, num_docs=55393) -> dict:
    """
    Computes TF-IDF scores for each URL based on query relevance.
    """
    return {
        url: sum(
            (1 + math.log(tf_t_d)) * math.log(num_docs / df_t)
            for word, tf_t_d, df_t in words if word in query
        )
        for url, words in url_word_freq.items()
    }

def merge_scores(url_word_freq: dict, query: list) -> list:
    """
    Function that generates the top 5 urls based on
    the average of pagerank and tfidf scoring methods
    """
    pagerank_scores = page_rank(url_word_freq, query)
    tfidf_scores = tf_idf(url_word_freq, query)

    final_scores = {}
    for url, tfidf_score in tfidf_scores.items():
        pagerank_score = pagerank_scores.get(url, 0)
        final_scores[url] = (tfidf_score + pagerank_score) / 2
 
    top_5 = []
    for _ in range(min(5, len(final_scores))):
        max_key = max(final_scores, key=final_scores.get)
        max_value = final_scores.pop(max_key)
        top_5.append((max_key, max_value))

    return top_5