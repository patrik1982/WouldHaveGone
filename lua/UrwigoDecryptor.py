import re

dtable = [chr(x) for x in range(1,128)]
decryptname = None

def luaToPython(s):
    res = ''

    res = s
    for k in range(32):
        res = res.replace('\\%03d' % (k), '\\x%02x' % (k))
    return eval(res)

def setLuaKeyString(str):
    setKey(luaToPython(str))

def setKey(table):
    global dtable
    dtable = table

def setDecryptFcnName(name):
    global decryptname
    decryptname = name

def getDecryptFcnName():
    global decryptname
    return decryptname

def decrypt(es):
    global dtable
    global decryptname
    if not decryptname:
        return es
    matchDecrypt = re.match('.*' + decryptname + '\("(.+)"\).*', es)
    if decryptname and matchDecrypt:

        #print("Encrypted fcncall '%s'" % (es))
        encryptedStr = '"' + matchDecrypt.group(1) + '"'
        e = encryptedStr
        #print("Encrypted string '%s'" % (encryptedStr))
        #print("Encrypted string '%s'" % (luaToPython(encryptedStr)))
        encryptedStr = encryptedStr.replace('\\127', chr(127))
        encryptedStr = encryptedStr.replace('\\195\\165', 'å')
        encryptedStr = encryptedStr.replace('\\195\\164', 'ä')
        encryptedStr = encryptedStr.replace('\\195\\182', 'ö')
        encryptedStr = encryptedStr.replace('\\194\\176', '°')
        s = luaToPython(encryptedStr)
        res = ''
        for i in range(len(s)):
            b = ord(s[i])
            if b > 0 and b <= 127:
                res = res + dtable[b-1]
            else:
                res = res + chr(b)
        #print("Decrypted string '%s'" % (res))
        #print(es)
        es = es.replace(e, res)
        es = es.replace(decryptname, '')
        es = es.replace('('+res+')', '"' + res + '"')
        if 'N 58' in es:
            pass
        #print("-->", es)
        #return res
        return es
    else:
        return es

