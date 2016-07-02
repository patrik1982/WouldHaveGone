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

def decrypt(str):
    global dtable
    matchDecrypt = re.match(decryptname + '\((.+)\)', str)
    if decryptname and matchDecrypt:
        #print("Encrypted fcncall '%s'" % (str))
        encryptedStr = matchDecrypt.group(1)
        #print("Encrypted string '%s'" % (encryptedStr))
        #print("Encrypted string '%s'" % (luaToPython(encryptedStr)))
        encryptedStr = encryptedStr.replace('\\127', chr(127))
        encryptedStr = encryptedStr.replace('\\195\\165', 'å')
        encryptedStr = encryptedStr.replace('\\195\\164', 'ä')
        encryptedStr = encryptedStr.replace('\\195\\182', 'ö')
        s = luaToPython(encryptedStr)
        res = ''
        for i in range(len(s)):
            b = ord(s[i])
            if b > 0 and b <= 127:
                res = res + dtable[b-1]
            else:
                res = res + chr(b)
        #print("Decrypted string '%s'" % (res))
        return res
    else:
        return str

