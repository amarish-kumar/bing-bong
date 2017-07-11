from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer

ps = PorterStemmer()

class InvertedIndex:
    inverted_index = {}

    @staticmethod
    def build_inverted_index(page_text, url):
        sentences = sent_tokenize(page_text)
        stop_words = set(stopwords.words('english'))

        result = []

        for sentence in sentences:
            word_tokens = word_tokenize(sentence)
            filtered_sentence = [ps.stem(w.lower()) for w in word_tokens if not w in stop_words]
            result += filtered_sentence

        set_words = set(result)
        for word in set_words:
            if word not in InvertedIndex.inverted_index:
                InvertedIndex.inverted_index[word] = []
            InvertedIndex.inverted_index[word].append(url)

    @staticmethod
    def get_rank(query):
        stop_words = set(stopwords.words('english'))
        # Spit words, and then stem them
        filtered_sentence = [ps.stem(w.lower()) for w in word_tokenize(query) if not w in stop_words]
        url_rank = {}
        for word in filtered_sentence:
            if word not in InvertedIndex.inverted_index:
                continue
            for url in InvertedIndex.inverted_index[word]:
                if url not in url_rank:
                    url_rank[url] = 0
                url_rank[url] += 1

        sorted_urls = sorted(url_rank.items(), key=lambda x: -x[1])
        return sorted_urls
