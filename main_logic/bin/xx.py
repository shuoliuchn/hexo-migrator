# print('a\n' in 'a\nbc')
# print('!dfajls'.split('!'))

# import re
# # s = r'![1570709244169](inherit.assets\1570709244169.png)'
# s = '<img src = "python-installation.assets/py_setup_01.png">'
# # re_str = '!\\[.+?\\]\\(.+?[.]assets.(.+?)\\..+?\\)'
# re_str = '<img src = .+?\\.assets.(.+?)\\..+?>'
# print(re.findall(re_str, s))

# import yaml
# s = """
# title: "技术查阅手册"
# date: 2020-02-16 14:36:06
# toc: true
# categories: 首页
# top: true
# layout: single-column"""
# # # with open(r'C:\Users\Sure\PyProject\神器\hexo-migration\linux\linux.md', 'r', encoding='utf8') as f:
# # #     y = yaml.load_all(f, yaml.FullLoader)
# y = yaml.load(s, yaml.FullLoader)
# print(y)
# d = {'title': '啦啦啦', '减少就收': '大大大'}
# print(yaml.dump(d))
# print(yaml.dump(y, encoding='utf8').decode('utf8'))

# import os
# os.path.relpat

# import re
# a = r'[二次编码](second-code.md#alex'
# # [二次编码](second-code.md)
#
# # link_re = '\\[.+?\\]\\(.*?[.]md\\)'
# link_re = '\\[.+?\\]\\(.*?\\.md[\\)#]'
# print(re.findall(link_re, a))

# from conf import settings
# print(settings.LOG_DIR)


# SAFE_BRACE = "{% raw %}%s{% endraw %}" % 'abc'
# print(SAFE_BRACE)


# print('' in ['1', 2])



# import string
# print(string.ascii_letters)


# import string
#
# def str_count(str):
#     '''找出字符串中的中英文、空格、数字、标点符号个数'''
#     count_en = count_dg = count_sp = count_zh = count_pu = 0
#
#     for s in str:
#         # 英文
#         if s in string.ascii_letters:
#             count_en += 1
#         # 数字
#         elif s.isdigit():
#             count_dg += 1
#         # 空格
#         elif s.isspace():
#             count_sp += 1
#         # 中文，除了英文之外，剩下的字符认为就是中文
#         elif s.isalpha():
#             count_zh += 1
#         # 特殊字符
#         else:
#             count_pu += 1
#
#     print('英文字符：', count_en)
#     print('数字：', count_dg)
#     print('空格：', count_sp)
#     print('中文字符：', count_zh)
#     print('特殊字符：', count_pu)
# s = 'dfajl!大家@发！# 管道·符了3 54沙3发开fs\][dj'
# str_count(s)

# def hanz_count(str):
#     hanz_total = 0
#     for s in str:
#         # 中文字符范围其实还有，但这些已经足够了
#         if '\u4e00' <= s <= '\u9fef':
#             hanz_total += 1
#     return hanz_total
#
# s = 'dfajl!大家@发！# 管道·符了3 54沙3发开fs\][dj'
# print(hanz_count(s))

# class A:
#     b = 11
#
# a = A()
# print(hasattr(a, 'b'))


# import os
#
# path = r'C:\Users\Sure\PyProject'
# dir = r'..\神器\hexo-migration\test'
# print(os.path.join(path, dir))

# a = 10
# a.bit_length = 11
# print(a.bit_length)

# def func():
#     return 123
#
# print(issubclass(func, object))
# s = '\nsjsjsjsjsjsjsjs\n'
# print(repr(s[2: -2]))
