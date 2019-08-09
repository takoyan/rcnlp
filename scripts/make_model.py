import codecs
import re
import MeCab
from gensim.models import word2vec

mt = MeCab.Tagger("")


def read_text(text_path):
    f = codecs.open(text_path, "r", "sjis")
    text_file = f.read()
    f.close()
    return text_file


def remake_text(pre_text):
    # remove header
    pre_text = re.split('\-{5,}', pre_text)[2]
    # remove bottom
    pre_text = re.split('底本：', pre_text)[0]
    # remove |
    pre_text = pre_text.replace('|', '')
    # remove rubi
    pre_text = re.sub('《.+?》', '', pre_text)
    # remove
    pre_text = re.sub('［＃.+?］', '', pre_text)
    # remove empty
    pre_text = re.sub("\n\n", "\n", pre_text)
    pre_text = re.sub("\r", "", pre_text)

    return pre_text


def select_word_class(word_class, documents_list):
    """
    get only specific word class from documents
    :param word_class: list
    :param documents_list: list
    :return: results_list: list
    """
    result_list = []
    results_list = []
    for document in documents_list:
        node = mt.parseToNode(document)
        while node:
            if node.feature.split(",")[0] in word_class:
                if node.feature.split(",")[6] == "*":
                    result_list.append(node.surface)
                else:
                    result_list.append(node.feature.split(",")[6])
            node = node.next
        results_list.append(result_list)
        result_list = []
    return results_list


def make_word2vec_model(txt_name):
    path = "../etc/txt/{}.txt".format(txt_name)
    text = read_text(path)
    text = remake_text(text)
    sentence_list = text.split("。")
    word_list = select_word_class(['名詞', '動詞'], sentence_list)
    model = word2vec.Word2Vec(word_list, size=100, min_count=5, window=5, iter=100)
    model.save("../etc/model/{}.model".format(txt_name))


if __name__ == "__main__":
    text_name = "sanshiro"
    # make_word2vec_model(text_name)
    model_sanshiro = word2vec.Word2Vec.load("../etc/model/{}.model".format(text_name))
    print(model_sanshiro.__dict__["wv"]["世間"])
    ren = model_sanshiro.wv.most_similar(positive=["世間"])
    for item in ren:
        print(item[0], item[1])
