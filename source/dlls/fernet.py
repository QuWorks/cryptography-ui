from cryptography import fernet


def Encrypt(key, filecontent):
    content = fernet.Fernet(key).encrypt(filecontent)
    return content


def Decrypt(key, filecontent):
    content = fernet.Fernet(key).decrypt(filecontent)
    return content
