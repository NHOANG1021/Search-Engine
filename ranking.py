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

def page_rank_weights(url_word_freq, url_tokens) -> list:
    """
    Returns a list of the weights of each token
    """
    weights = []
    for url, token in url_tokens:
        weight = []
        for posting in url_word_freq[url]:
            weight_value = posting[1] / token
            weight_value =  round(weight_value, 2)
            
            weight.append(round(weight_value, 2))
        weights.append(weight)
    
    return weights

def page_rank(url_word_freq, weights, query) -> list[tuple[str, int]]:
    """
    Grants a score for each url based off of a word's weight
    and how much in appears in comparision to the query
    """
    scores = {}
    
    for i, (url, words) in enumerate(url_word_freq.items()):
        score = 0
        for j, (word, freq) in enumerate(words):
            if word in query:
                # Multiply frequency by corresponding weight
                score += freq * weights[i][j]
        scores[url] = score
    
    # Sort URLs by their computed scores in descending order
    ranked_urls = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    return ranked_urls