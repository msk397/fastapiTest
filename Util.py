import base64

from idna import unicode

import hashlib
# 获取首字母
def FirstPinyin(str):
    from xpinyin import Pinyin
    p = Pinyin()
    return p.get_initials(str, u'')

#生成MD5
def MD5(str):
    md= hashlib.md5()# 创建md5对象
    md.update(str.encode(encoding='utf-8'))
    return md.hexdigest()

#生成密码
def setPass(id,name):
    id = id[0:5]
    name = name
    passwd =id+FirstPinyin(name)
    return [passwd,MD5(passwd)]

#处理业主地址
def addr(str):
    addrlist = str.split('-', 2)
    a = addrlist[0]
    b= addrlist[1]
    c= addrlist[2]
    return a + '号楼' + b + '单元' + c



