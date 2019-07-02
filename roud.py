#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
import treetaggerwrapper as ttw
from select_txt import get_wordsurface
#import gensim

TTWDIR='/home/takoyan/tree-tagger-install'
tagger=ttw.TreeTagger(TAGLANG='en', TAGDIR=TTWDIR)
#model=gensim.models.KeyedVectors.load_word2vec_format('~/word2vec/word2vec/wiki.bin', binary=True, unicode_errors='ignore')



#wordをkeyとして出現回数をvalueとする辞書
def word_count(text):
    dic = {}
    word_list = text.split()
    for word in word_list:
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1
    return dic

#複数の文書を格納したリストに対するワードカウント
def multi_word_count(text_list):
    dic={}    #最終的な辞書
    temp_dic={}    #一時的な辞書
    for line in text_list:
        temp_dic=word_count(line)
        for key_word in temp_dic:
            if key_word in dic:
                dic[key_word]+=temp_dic[key_word]
            else:
                dic[key_word]=1
    return dic
                

# 文を表層系にする関数
def get_surface_text(text):
    flag = False
    tags = tagger.TagText(text.decode("utf-8"))
    for tag in tags:
        word = tag.split('\t')[2] # 表層系
        word = word.encode("utf-8")
        if flag == False:#一周目のみ例外処理
            line = word
            flag = True
        else:
            line = line + " " + word
    return line



#正誤が混ざったテキスト郡から正解文のみを表層系にして返す.
def get_answer_txt(txt_list):
    loop_count=1
    answer_list=[]
    for line in txt_list:
        if(loop_count % 6 == 1):
            line = line.rstrip('\n') #改行でスプリット
            line = get_surface_text(line)
            answer_list.append(line)
        loop_count+=1
    return answer_list

#1本の文章と単語を入力としてtfの値を求める
def calc_tf(txt, word):
    tf_score=1 + math.log(word_count(txt)[word], 2)
    return tf_score

#複数の文章と単語を入力としてidfの値を求める
def calc_idf(txt_list, word):
    ans_word_count={}
    ans_word_count=multi_word_count(txt_list)
    if(word in ans_word_count) == False:
        ans_word_count[word] = 0
    if(ans_word_count[word] >= len(txt_list)):
        ans_word_count[word] = len(txt_list)-2
    idf_score=math.log(float(len(txt_list)) / float(ans_word_count[word] +1.0), 2) #theが来ると値がマイナスとなる
    return idf_score
    
# 2つの文章に対してコサイン類似度を計算する.
# cos類似度計算に問題あり
def cos_sim(a, txt_list):
    cos = 0.0
    dic = {}    #入力文のword_count格納
    dic2 = {}    #正解文のword_count格納
    result = []
    dic=word_count(a)
    length_d = 0.0
    for d in dic:
        #try:
        weight = calc_tf(a, d) * calc_idf(txt_list, d) #* model.similarity(d, get_special_word(a, txt_list))
        #length_d += (dic[d] * weight)**2
        length_d += dic[d]**2
        """
        except:
            length_d += (dic[d] * calc_tf(a, d) * calc_idf(txt_list, d) * 0.1)**2
        """
    length_d = math.sqrt(length_d)    #入力文に対する分母値

        
    for line in txt_list:
        length_d2 = 0.0
        dic2 = word_count(line)    #正解文の1文ずつに対してword_countを行う.
        for d2 in dic2:
            #try:
            weight2 = calc_tf(line, d2) * calc_idf(txt_list, d2)# * model.similarity(d2, get_special_word(line, txt_list))
            #length_d2 += (dic2[d2] * weight2)**2
            length_d2 += dic2[d2]**2
            """
            except:
            length_d2 += (dic2[d2] * calc_tf(line, d2) * calc_idf(txt_list, d2) * 0.1)**2
            """
        length_d2 = math.sqrt(length_d2)    #正解文に対する分母値

        score = 0.0
        for d in dic:
            if d in dic2:
                #score += (dic[d] * weight) * (dic2[d] * weight2)    #分子の掛け算
                score += dic[d] * dic2[d]
        if score != 0.0:
            cos = float(score) / float(length_d * length_d2)
        result.append(cos)
        score=0.0
        cos=0.0
        
    return txt_list[result.index(max(result))]

#入力された文章に対して最もtfidf値が高い単語を返す
def get_special_word(txt, ans_list):
    tfidf_list=[]
    for word in txt.split(' '):
        tfidf_list.append(calc_tf(txt, word) * calc_idf(ans_list, word))
    return txt.split(' ')[tfidf_list.index(max(tfidf_list))]


if __name__=='__main__':
    surface_txt_list=[]    #全文章の表層系を格納
    with open('question_wrong.txt', 'r') as qw_txt:
        for line in qw_txt:
            #全文章を表層系へと変換
            surface_txt_list.append(get_surface_text(line))
    answer_list = get_answer_txt(surface_txt_list)    #正解文を格納したリスト
    count = 1
    score = 0
    
    for line in surface_txt_list:
        if(count % 6 == 1):
            ans_txt = line    #類似度計算の正解文
            count += 1
        else:
            calced_txt=cos_sim(line, answer_list)    #類似度計算で得られた文章
            print('input: '+line)
            print('========================')
            print('ans_txt :' + ans_txt)
            print('calced :' + calced_txt)
            print('========================')
            print('\n')
            if(ans_txt==calced_txt):
                score+=1
            print(score)
            count += 1
    
    
    
