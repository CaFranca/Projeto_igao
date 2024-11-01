import hashlib
senha="Cinema"
crip=hashlib.sha256(senha.encode()).hexdigest()
print(crip)