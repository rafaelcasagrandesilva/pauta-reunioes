import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha, hash):
    return hashlib.sha256(senha.encode()).hexdigest() == hash