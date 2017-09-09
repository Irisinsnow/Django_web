from _sha1 import sha1


def get_hash(str, salt=None):
    """
    对密码进行加密的实现
    """
    str = '!@#$%'+str+'^&*)('
    if salt:
        str += salt

    sh = sha1()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()
