from idna import unicode
from xpinyin import Pinyin
import hashlib
# 获取首字母
def FirstPinyin(str):
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
