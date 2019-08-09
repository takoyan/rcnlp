import gensim
from gensim import corpora
from collections import defaultdict
from prepare_txt import select_word_class, remove_stop_word, read_stop_words_txt

def count_word(words_list):
    """
    count number of words
    :return word_count: dict
    :param words_list: list
    """
    word_count = defaultdict(int)
    for document in words_list:
        for word in document:
            word_count[word] += 1
    return word_count


def remove_low_frequency_words(documents_list, freq_list):
    """
    remove words which are low frequency
    :return result: list
    :param documents_list: list
    :param freq_list: dict
    """
    threshold = 1
    return [[word for word in document if freq_list[word] > threshold] for document in documents_list]


if __name__ == "__main__":
    documents = ["【平日限定】15時まで滞在可！乾杯酒＆食後のカフェフリー！サラダブッフェや選べるメイン",
                 "【平日限定】15時まで滞在可！乾杯酒＆食後のカフェフリー！国産安心野菜ブッフェとパスタ＋選べるメイン",
                 "【9周年記念】ロッシーニを含むフルコースにGスパーク＆お好みの1ドリンク！SNSで人気のフラワーケーキ付！",
                 "【川床席確約】土日祝限定！記念日利用ならケーキも！前菜、パスタ、メイン、デザートなど全5品！",
                 "【タイムセール】ロゼスパークリング含む3時間飲み放題！お肉アップグレードのメインや季節のデザート等7品",
                 "【タイムセール】120フリードリンク・お魚とお肉をチョイスで楽しめるミケーレコース　組数限定特別プラン",
                 "【タイムセール】川床席×乾杯シャンパン付！小鮎の前菜、冬瓜のスープ、魚＆肉のWメイン、デザートの全5品",
                 "東京のレトロな喫茶店でコーヒースイーツを満喫「銀座和蘭豆」",
                 "東京でふわふわなわたあめスイーツを堪能しよう"]

    input_text = ["皿盛りデザートを肉やワインと共にいただける"]

    # ####### preparing text ##############

    # documents = remove_stop_words(["名詞", "形容詞", "形容動詞"], documents)
    documents = select_word_class(["名詞", "形容詞", "形容動詞"], documents)
    documents = remove_stop_word(documents)
    frequency = count_word(documents)
    dictionary = corpora.Dictionary(documents)
    # dictionary.save("../etc/freq.dict")
    corpus = [dictionary.doc2bow(document) for document in documents]
    # corpora.MmCorpus.serialize("../etc/corpus/freq.mm", corpus)

    #########################################

    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=3, id2word=dictionary)
    for lda_result in lda.show_topics():
        print(lda_result)
    input_text = select_word_class(["名詞", "形容詞", "形容動詞"], input_text)
    input_text = remove_stop_word(input_text)
    print(input_text)
    test_corpus = [dictionary.doc2bow(text) for text in input_text]
    for probability_per_doc in lda[test_corpus]:
        print(probability_per_doc)
