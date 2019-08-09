import MeCab
import pandas as pd


def select_word_class(word_class, documents_list):
    """
    get only specific word class from documents
    :param word_class: list
    :param documents_list: list
    :return: results_list: list
    """
    mt = MeCab.Tagger("")
    result_list = []
    results_list = []
    for document in documents_list:
        node = mt.parseToNode(document).next
        while node.next:
            if node.feature.split(",")[0] in word_class:
                if node.feature.split(",")[6] == "*":
                    result_list.append(node.surface)
                else:
                    result_list.append(node.feature.split(",")[6])
            node = node.next
        results_list.append(result_list)
        result_list = []
    return results_list


def remove_stop_word(document_list):
    """
    remove stop-words from documents
    :param document_list: list
    :return: list
    """
    stop_words = read_stop_words_txt()
    return [[word for word in document if word[0] not in stop_words] for document in document_list]


def read_stop_words_txt():
    stop_words_list = []
    f = open("../etc/txt/stop_words.txt", "r")
    words = f.readlines()
    f.close()
    for word in words:
        stop_words_list.append(word.split("\n")[0])
    return stop_words_list


if __name__ == "__main__":
    # txt = ["テキストデータを一件ずつ分かち書き,すごい",
    # "七つの海の楽園嵐の夜の後には 愛を伝えるため 命がまた生まれる 7つの国のメロディア誰もが いつかはここを 旅立つ日が来ても 私は 忘れない"]
    f = open("../etc/txt/item_name_list.csv", "r")
    lines = f.readlines()
    f.close()
    new_txt = select_word_class(["名詞, 形容詞, 形容動詞"], lines)
    new_txt = remove_stop_word(new_txt)
    df = pd.DataFrame({"item_name": new_txt})
    df.to_csv("../etc/txt/cleaned_item_name_.csv", header=False, index=False)
