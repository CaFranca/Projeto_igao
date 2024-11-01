import hashlib
senha="que"
crip=hashlib.sha256(senha.encode()).hexdigest()
print(crip)