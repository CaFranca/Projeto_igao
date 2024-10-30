import hashlib
senha="Caique"
crip=hashlib.sha256(senha.encode()).hexdigest()
print(crip)