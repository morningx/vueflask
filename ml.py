import jieba
import numpy as np
from collections import Counter


# https://blog.csdn.net/weixin_43734080/article/details/121432656
# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('./stopword/stopwords_stand_last.txt',encoding='UTF-8').readlines()]
    # print("stopwords:::",stopwords[0:30])
    # stopwords::: ['--', 'csdn', 'net', '?', '<', '>', '!', ',', '.', '"', '/', '~', '`', '-', '=', '+', '(', ')', '*', ':', ';', '－－', '、', '。',, '”', '《', '》', '（', '）']
    return stopwords

# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    # print("正在分词")
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''
    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word not in [ str(i) for i in range(10)] or \
               word not in [ i for i in range(10)] :
                outstr += word
                outstr += " "
    return outstr

def jieba_example():
    seg_list = jieba.cut("中国深圳是一座美丽的国际性大都市城市在不断升维，人在深圳存在的价值感升维，证明了中国现代化解放人性和创新政策机制的可能性，积攒了难得的包容、责任、情怀、奉献、人文主义等，留下了四十年不可逆的深圳进步历史，人们用“一夜城”和“速生城市”形容深圳城市建设的奇迹，。“来了就是深圳人！”显现了深圳社会迸发的生命力，也预示了这座移民城市未来的不确定性……中国深圳是一座美丽的国际性大都市中国深圳是一座美丽的国际性大都市", cut_all=True)
    # print("Full Mode: " + "/ ".join(seg_list))
    # Full Mode: 中国/ 深圳/ 是/ 一座/ 美丽/ 的/ 国际/ 国际性/ 大都/ 大都市/ 都市
    jblis = str("/ ".join(seg_list)).replace(" ","").split("/")
    # print(jblis)
    # return jblis
    # 将解析出来的词汇进行踢出stopwords处理
    ressw = []
    for i in jblis:
        resi = seg_depart(i)
        if len(resi) != 0:
            ressw.append(resi)

    ressw = np.array(ressw)
    cnt_res_jieba_stopwords = Counter(ressw)
    # print('Counter(jblis):::',Counter(jblis)) # 调用Counter函数
    # res_jieba_cnt_res_jieba_stopwords::: Counter({'深圳 ': 8, '中国 ': 4, '城市 ': 4, '一座 ': 3, '美丽 ': 3, '国际 ': 3, '国际性 ': 3, '大都 ': 3,  3, '升 ': 2, '维 ': 2, '人 ': 2, '价值 ': 1, '感 ': 1, '证明 ': 1, '现代化 ': 1, '化解 ': 1, '解放 ': 1, '人性 ': 1, '创新 ': 1, '新政 ': 1, '政性 ': 1, '积攒 ': 1, '难得 ': 1, '包容 ': 1, '责任 ': 1, '情怀 ': 1, '奉献 ': 1, '人文 ': 1, '人文主义 ': 1, '主义 ': 1, '留下 ': 1, '四十 ': 1, ': 1, '历史 ': 1, '一夜 ': 1, '城 ': 1, '速生 ': 1, '形容 ': 1, '建设 ': 1, '奇迹 ': 1, '显现 ': 1, '社会 ': 1, '迸发 ': 1, '生命 ': 1, '生命力, '移民 ': 1, '移民城市 ': 1, '未来 ': 1, '不确定性 ': 1, '确定性 ': 1, '定性 ': 1, '… … ': 1})
    tuple_list_cnt_res_jieba_stopwords = []
    for i in cnt_res_jieba_stopwords:
        # print(i,cnt_res_jieba_stopwords[i])
        # tuple_list_cnt_res_jieba_stopwords::/n [('中国 ', 4), ('深圳 ', 8), ('一座 ', 3), ('美丽 ', 3), ('国际 ', 3), ('国际性 ', 3), ('大都 ', 3), ('大, 3), ('城市 ', 4), ('升 ', 2), ('维 ', 2), ('人 ', 2), ('价值 ', 1),
        tuple_list_cnt_res_jieba_stopwords.append((i,cnt_res_jieba_stopwords[i]))
    return tuple_list_cnt_res_jieba_stopwords

def jieba_WordCloudData(word_cloud_data):
    word_cloud_data = word_cloud_data
    seg_list = jieba.cut(word_cloud_data,cut_all=True)
    # print(str(len("#######".join(seg_list)))+ "Full Mode: " + "#######".join(seg_list))
    jblis = "$".join(seg_list).replace(" ","").replace(",","").replace("csdn","哈哈哈").split("$")
    # print(len(jblis),type(jblis),'jblis:::',jblis)
    # 将解析出来的词汇进行踢出stopwords处理
    stopwords = stopwordslist()
    ressw = []

    lis_letter_num_biglow = []
    lis_letter_low = [chr(i) for i in range(97,123)]
    lis_letter_upper = [ j.upper() for j in ([chr(i) for i in range(97,123)]) ]
    lis_num_str = [str(i) for i in range(0,10)]
    # print(lis_num_str)
    lis_num_int = [i for i in range(0,10)]
    lis_letter_num_biglow.extend(lis_letter_low)
    lis_letter_num_biglow.extend(lis_letter_upper)
    lis_letter_num_biglow.extend(lis_num_int)
    lis_letter_num_biglow.extend(lis_num_str)
    # print("lis_letter_num_biglow:::",type(lis_letter_num_biglow),lis_letter_num_biglow)
    #   ('lis_letter_num_biglow:::', <type 'list'>, ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

    for i in jblis:
        if i not in stopwords and len(list(set(i) - set(lis_letter_num_biglow))) != 0:
        #    and i not in [ str(j) for j in range(10000)] \
        #    and i not in [ j for j in range(10000)] \
        #   and i not in [ chr(j).upper() for j in range(97,123)] \
        #    and i not in [ chr(j) for j in range(97,123)]:
            # print("i:::",i)
            ressw.append(i)
    # print("ressw:::",ressw)
    ressw = np.array(ressw)

    cnt_res_jieba_stopwords = Counter(ressw)
    tuple_list_cnt_res_jieba_stopwords = []
    for i in cnt_res_jieba_stopwords:
        tuple_list_cnt_res_jieba_stopwords.append((i,cnt_res_jieba_stopwords[i]))
    return tuple_list_cnt_res_jieba_stopwords


if __name__ == "__main__":

    # 全模式
    tuple_list_cnt_res_jieba_stopwords = jieba_example()
    # print("tuple_list_cnt_res_jieba_stopwords::/n",tuple_list_cnt_res_jieba_stopwords)
    # tuple_list_cnt_res_jieba_stopwords::/n [('中国 ', 4), ('深圳 ', 8), ('一座 ', 3), ('美丽 ', 3), ('国际 ', 3), ('国际性 ', 3), ('大都 ', 3), ('大, 3), ('城市 ', 4), ('升 ', 2), ('维 ', 2), ('人 ', 2), ('价值 ', 1),