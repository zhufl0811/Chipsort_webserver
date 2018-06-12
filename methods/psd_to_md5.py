import hashlib

def psd_to_md5(psd):
    md5_str = hashlib.md5(psd.encode('utf-8'))
    result = md5_str.hexdigest()
    return result

if __name__ == '__main__':
    print(psd_to_md5('admin'))