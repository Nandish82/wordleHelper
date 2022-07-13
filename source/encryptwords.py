import base64

def encrypt_word(word):
    word_bytes=word.encode('ascii')
    base64_bytes=base64.b64encode(word_bytes)
    base64_message=base64_bytes.decode('ascii')
    return base64_message

def decrypt_word(base64_message):
    base64_bytes=base64_message.encode('ascii')
    message_bytes=base64.b64decode(base64_bytes)
    message=message_bytes.decode('ascii')
# encoding

f=open('wordle-nyt-allowed-guesses.txt','r')
f2=open('encrypted-allowed-guesses.txt','w')
for line in f:
    t=line.split()
    word_encrypt=encrypt_word(t[0])
    f2.write(word_encrypt)
    f2.write('\n')

f.close()
f2.close()
