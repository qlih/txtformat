#!/usr/bin/env python3
# Encoding:UTF-8
#	hnv_unwrap.py
#	算法描述：
#	utf-8格式读入
#		测量长度，一般字符算1，CJK算2，各行的长度都统计后，排序。相对多字符（比如多余56个ascii），最长的行，如果不多，则可以忽略，看某一个宽度，如70字宽的行是不是很多。
#		如果确定是 wrap 的格式，则
#			干掉折行，不论结尾的地方是否有标点；
#			不是标点符号结尾的，unicode Po等，长度短于 wrap 值不多的，如20%，折，少的，发警告。按照预设，应该也折。可能出现错误，如诗歌什么的。
#		特殊的符号是否处理？比如：「」转换为：“”。
#       有的时候，源文件会漏掉行尾的标点。比如标题，比如《完》什么的。

__author__ = 'qlih@qq.com'
__version__ = '0.01'

import re
import os
import sys
import codecs

class textUnWrap():

    __lines=[]  # 原始数据
    __textFileName=''
    __outDir='./1/' # 默认的输出目录

    __txt=[]    # 保存处理结果

    __writed = False    # 避免重复写盘

    def __init__ (self, filename='demo_wrap.txt', codeType='utf-8'):
        print(filename)
        print(codeType)

        __lines=[]
        __textFileName=''
        if codeType=='':
            codeType='utf-8'
        elif codeType=='GB2312' or codeType=='GBK':
            codeType='GB18030'
        with codecs.open(filename,'r', encoding=codeType) as f:
            try:
                self.__lines = f.readlines()
            except Exception as e:
                print(e)    # 一般来说，发生错误后，就不会继续处理了。
                pass
#                raise
            else:
                pass
            finally:
                pass

            self.__textFileName=filename
            self.__txt =[]
        pass

    def close(self):
        # write to file.
        f=open(self.__outDir+self.__textFileName,'w')  #默认存盘的字符编码是utf8，mac下测试。
        for lc in self.__txt:
            f.write(lc)
        f.close()
        #print(self.__txt)

    # .basic() 方法需要人工识别。
    def basic(self):    # 最简单的情况：2个全角空格开始……直到下一个2个全角空格开始的行，中间的换行全删掉。

        # 这里要设置一个例子，说明到底能处理哪种状况。

        _tmpLine=''     # 自然段，缓存。
        _newLine = False

        for lc in self.__lines:
            # 每一行的缓存，可以去读区规则区的规则，轮番适配一下。
            if re.search('^　　[^　 ]',lc, re.I):  # \u#3000
                        # 应该 增加一个 四半角空格 的选项。
                if _newLine:    # 两个紧邻的自然段。等于要换行（新段落）了。
                    _tmpLine=_tmpLine+os.linesep

                self.__txt.append(_tmpLine)

                _tmpLine='　　'+lc.strip()    # '\u3000\u3000'
                _newLine=True
            elif lc==os.linesep:    # basic版：空行，就是自然段结束。
                if _newLine:
                    _tmpLine=_tmpLine+os.linesep
                    _newLine=False

                    # 改进：每一行都要单独的append一次。这样的self.__txt是。readlines()的格式。

                _tmpLine=_tmpLine+os.linesep
                self.__txt.append(_tmpLine)
                _tmpLine=''
            else:
                if _newLine:    # 自然段的非首行。
                    _tmpLine=_tmpLine+lc.rstrip()
                else:   # 不是自然段内，不处理。
                    _tmpLine=_tmpLine+lc
        # 最后一行。
        self.__txt.append(_tmpLine)

    def reset(self):
        self.__txt = []

        pass

    def advance(self):  # 计算每行的长度。
        # 1 用 muilti_line模式，搜索 标题、独立行……替换成特色【】包含符号。
        # 2 整理 其他剩下的段落，行程新的自然段。
        pass

    def getFilename(self):
        # print(self.__textFileName)
        return self.__textFileName

    def setOutDir(self, outDir='./'):
        self.__outDir = outDir
        pass


import chardet
#import codecs

if __name__ == '__main__':
    i =len(sys.argv)
    # print(len(sys.argv)) # macOS bash 会把 *.* 里面的文件名都展开。
    if i>1: # 如果有参数，要从第一个文件开始计算，或者先装入一个列表。
        while i>1:  # 参数是'*.*'时，shell会自动展开*.*，所以用循环。
            finput = open(sys.argv[i-1], 'rb')
            codeType = chardet.detect(finput.read(1024))["encoding"]    #检测编码方式，读4K就可以了。也许1024
            print ('编码是 ', codeType)
            finput.close()

            unwrap = textUnWrap(sys.argv[i-1],codeType)
            unwrap.basic()
            unwrap.close()  # 写盘
            i=i-1
    else:
        print('Usage example: unwrap.py *.txt')
