'''//////////////////////////////
        Antes de executar o programa é necessário instalar o Flask e o Sympy, podem ser instalados pelos comandos:
        - pip install flask
        - pip install sympy
        Após a execução, o programa estará sendo executado em http://127.0.0.1:5000
   //////////////////////////////'''

from flask import Flask, render_template, request, session
from sympy import isprime
import random
import math

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Jk1.Z)&,fl2:1s;nWghB!!V9tc`d11l@eod-A6I1(>r£'

carac = ' abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-çãáàíéóúâõê!@#$%&()/\|?;:0123456789+*,.<>=º°ª[]{}'
carac_dict = {}

for i, letter in enumerate(carac, start=10):
    carac_dict[letter] = i

def totient(p, q):
    return (p - 1) * (q - 1)

def primo(n):
    if isprime(n):
        return True
    else:
        return False

def gera_primo():
    while True:
        x = random.randrange(256, 1000)
        if(primo(x) == True):
            return x

def gera_e(n_toti):
    while True:
        x = random.randrange(1, n_toti + 1)
        if math.gcd(n_toti, x) == 1:
            return x

def encrypt(frase, e, n):
    lst = []
    invalid_characters = []

    for letra in frase:
        if letra in carac_dict:
            numero = carac_dict[letra]
            num_crypt = pow(numero, e, n)
            lst.append(num_crypt)
        else:
            invalid_characters.append(letra)

    if invalid_characters:
        return lst, invalid_characters
    else:
        return lst, []

def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def privkey(e, n_toti):
    d = modinv(e, n_toti)
    return d

def decrypt(ciphertext, d, n):
    original_msg = []
    for num_crypt in ciphertext:
        num_orig = pow(num_crypt, d, n)
        for letra, numero in carac_dict.items():
            if numero == num_orig:
                original_msg.append(letra)

    return ''.join(original_msg)

@app.route('/')
def index():
    return render_template('index.html', frase_digitada="", frase_criptografada="")

@app.route('/decryptpage')
def decryptpage():
    return render_template('decrypt.html', decrypted="")

@app.route('/encrypt', methods=['POST'])
def encrypt_message():
    frase = request.form['text']
    p = gera_primo()
    q = gera_primo()
    n = p * q
    n_toti = totient(p, q)
    e = gera_e(n_toti)
    encrypted, invalid_characters = encrypt(frase, e, n)
    
    if invalid_characters:
        error_message = "Caracteres inválidos: " + ", ".join(invalid_characters)
        return render_template('index.html', frase_digitada=frase, frase_criptografada="", error_message=error_message)
    else:
        d = privkey(e, n_toti)
        session['n'] = n
        session['d'] = d
        return render_template('index.html', frase_digitada=frase, frase_criptografada=', '.join(map(str, encrypted)), error_message="")


@app.route('/decrypt', methods=['POST'])
def decrypt_message():
    ciphertext = request.form['ciphertext']
    n = session.get('n')
    d = session.get('d')
    ciphertext = [int(x) for x in ciphertext.split(', ')]
    decrypted_message = decrypt(ciphertext, d, n)

    return render_template('decrypt.html', decrypted=decrypted_message)

if __name__ == '__main__':
    app.run(debug=True)