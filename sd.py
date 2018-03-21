#!/usr/bin/env python3
# Encoding:UTF-8


"""
全角半角转换
    SBC case 全角
    DBC case 半角
    全角-半角 == 0xfee0
    Alpha: A, \uFF21, \u0041 - Z, \uFF3A, \u005A
    Alpha: a, \uFF41, \u0061 - z, \uFF5A, \u007A
    Digital: 0, \uFF10,\u0030 - 9 , \uFF19, \u0039
"""

__author__ = 'qlih@qq.com'
__version__ = '0.01'

import logging
logger = logging.getLogger("TSF")
stagelog = logging.getLogger("stageParse")

Alpha = 0x10
Digital = 0x100

def sdb2dbc(src, mode=Alpha|Digital):
    count = 0
    ret = ''

    modeAlhpa = False
    modeDigital = False

    if mode & Alpha == Alpha:
        modeAlhpa = True
    if mode & Digital == Digital:
        modeDigital = True

    for uchar in src:
        uCode=ord(uchar)
        if ((uCode>=0xff21 and uCode<=0xff3a)and modeAlhpa) or \
            (((uCode>=0xff41 and uCode<=0xff5a ) or (uCode>=0xff10 and uCode<=0xff19)) and modeDigital):
            ret +=chr(uCode-0xfee0)
            count+=1
        else:
            ret += uchar

    return count,ret
