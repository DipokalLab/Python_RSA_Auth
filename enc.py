"""
 ____    _____  ____      __ __    ___  ____   ____  _____  ____   __   ____  ______  ____  ___   ____  
|    \  / ___/ /    |    |  |  |  /  _]|    \ |    ||     ||    | /  ] /    ||      ||    |/   \ |    \ 
|  D  )(   \_ |  o  |    |  |  | /  [_ |  D  ) |  | |   __| |  | /  / |  o  ||      | |  ||     ||  _  |
|    /  \__  ||     |    |  |  ||    _]|    /  |  | |  |_   |  |/  /  |     ||_|  |_| |  ||  O  ||  |  |
|    \  /  \ ||  _  |    |  :  ||   [_ |    \  |  | |   _]  |  /   \_ |  _  |  |  |   |  ||     ||  |  |
|  .  \ \    ||  |  |     \   / |     ||  .  \ |  | |  |    |  \     ||  |  |  |  |   |  ||     ||  |  |
|__|\_|  \___||__|__|      \_/  |_____||__|\_||____||__|   |____\____||__|__|  |__|  |____|\___/ |__|__|
                                                                                                        Developer: DipokalHHJ
"""

import hashlib
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import os.path



def createHash(data):
    h = hashlib.sha256()
    h.update(data)
    res = h.hexdigest()
    return res

def createPrivatekey():
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    return key

def createAuthInfo(data):
    # data [id, pw]
    splitNumber = '.'
    return splitNumber.join(data)

def savePrivatekey(key, hashd):
    filedir = './key/'+hashd+'.pem'
    with open (filedir, "w") as prv_file:
        print("{}".format(key.exportKey()), file=prv_file)

def loadPrivatekey(name):
    filedir = './key/'+name+'.pem'
    if os.path.isfile(filedir):
        f = open(filedir, 'r')
        return RSA.importKey(f.read())
        f.close()
    else:
        return '0'


def verification(encdata, user):
    message = encdata
    # message = 원본 데이터의 해시를 암호화 한 값
    hashinfo = createHash(createAuthInfo(user).encode('utf-8'))
    key = loadPrivatekey('k')
    decrypted = key.decrypt(ast.literal_eval(str(message)))
    # decrypted = 해시
    # print(hashinfo.encode('utf-8'), decrypted, type(key))
    if type(key) is str:
        print("NN")
    else:
        if decrypted == hashinfo.encode('utf-8'):
            print("Y") # 로그인 성공
        else:
            print('N')


def changeBinary(text):
    return text.strip()

def createUser(userid, userpw):
    key = loadPrivatekey('k')

    authinfo = createAuthInfo([userid, userpw])
    authinfohash = createHash(authinfo.encode('utf-8'))

    publickey = key.publickey()
    encrypted = publickey.encrypt(authinfohash.encode('utf-8'), 32)
    f = open ('./enc/'+userid+'.txt', 'w')
    f.write(str(encrypted))
    f.close()

def main():
    userid = '3457xc'
    userpw = 'asdf1234'
    createUser(userid, userpw)

    '''
    # 개인 키 생성
    # key = createPrivatekey()

    # 개인 키 불러오기
    key = loadPrivatekey('k')
    userid = '3457xc'
    userpw = 'asdf1234'

    authinfo = createAuthInfo([userid, userpw])
    authinfohash = createHash(authinfo.encode('utf-8'))
    # savePrivatekey(key, authinfohash)
    # print("K", changeBinary(key.exportKey()))

    # 공개 키
    publickey = key.publickey()
    encrypted = publickey.encrypt(authinfohash.encode('utf-8'), 32)
    f = open ('./enc/'+userid+'.txt', 'w')
    f.write(str(encrypted))
    f.close()
    '''

    # 해독
    f = open('./enc/'+userid+'.txt', 'r')
    message = f.read()

    '''
    decrypted = key.decrypt(ast.literal_eval(str(encrypted)))
    print ('decrypted', decrypted)
    f = open ('dec.txt', 'w')
    f.write(str(decrypted))
    f.close()
    '''

    # 검증
    verification(message, ['3457xc', 'asdf1234'])

if __name__ == '__main__':
    main()


