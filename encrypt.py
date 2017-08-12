import rsa
import binascii


def get_sp(pubkey, servertime, nonce, password):
    rsaPublicKey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublicKey, 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    sp = binascii.b2a_hex(rsa.encrypt(message.encode(encoding='utf-8'), key))
    return sp
