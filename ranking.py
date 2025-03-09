import math


def page_rank_tokens(url_word_freq) -> list:
    """
    Return a list of total number of tokens in a url
    """
    result = []
    for url, postings in url_word_freq.items():
        total = 0
        for posting in postings:
            total += posting[1]

        data = url, total
        result.append(data)

    return result

def page_rank_weights(url_word_freq) -> list:
    """
    Returns a list of the weights of each token
    """
    weights = []
    url_tokens = page_rank_tokens(url_word_freq)
    for url, token in url_tokens:
        weight = []
        for posting in url_word_freq[url]:
            weight_value = posting[1] / token
            weight_value =  round(weight_value, 2)
            
            weight.append(round(weight_value, 2))
        weights.append(weight)
    
    return weights

def page_rank(url_word_freq, query) -> list[tuple[str, int]]:
    """
    Grants a score for each url based off of a word's weight
    and how much in appears in comparision to the query
    """
    scores = {}
    weights = page_rank_weights(url_word_freq)
    
    for i, (url, words) in enumerate(url_word_freq.items()):
        score = 0
        for j, (word, freq, df) in enumerate(words):
            if word in query:
                # Multiply frequency by corresponding weight
                score += freq * weights[i][j]
        scores[url] = score
    
    return scores


def tf_idf(url_word_freq,  query, num_docs=55393):
    tf_idf_scores = {}

    for url, words in url_word_freq.items():
        total_score = 0
        for word, tf_t_d, df_t in words:  
            if word in query:
                tf = 1 + math.log(tf_t_d)
                idf = math.log(num_docs / df_t)
                total_score += tf * idf

        tf_idf_scores[url] = total_score
    

    return tf_idf_scores


def merge_scores(url_word_freq, query):
    pagerank_scores = page_rank(url_word_freq, query)
    tfidf_scores = tf_idf(url_word_freq, query)
    final_scores = {}

    for url, tfidf_score in tfidf_scores.items():
        pagerank_score = dict(pagerank_scores).get(url, 0)
        final_scores[url] = tfidf_score * pagerank_score

    sorted_final_scores = dict(sorted(final_scores.items(), key=lambda item: item[1], reverse=True))

    return sorted_final_scores




