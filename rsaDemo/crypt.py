import random, os
from . import genLargePrimes

def Extended_euclid(a, b):
	x0, x1, y0, y1 = 0, 1, 1, 0

	while a != 0:
		q, b, a = b//a, a, b%a
		y0, y1 = y1, y0 - q*y1
		x0, x1 = x1, x0 - q*x1

	return b, x0, y0


def generatePublicKey(totient):
	public_key = random.randrange(3, totient)
	while not genLargePrimes.is_prime(public_key):
		print("Generating public key : ", public_key)
		public_key += 1
	return public_key


def generatePrivateKey(public_key, totient):
	g, _, private_key = Extended_euclid(int(totient), int(public_key))
	if private_key > totient:
		private_key = private_key % totient
	elif private_key < 0:
		private_key += totient
	return private_key

def runRSA(message, bits):
	p = genLargePrimes.generate_prime_number(bits)
	q = genLargePrimes.generate_prime_number(bits)
	n = p*q
	totient = (p-1)*(q-1)
	public_key = generatePublicKey(totient)
	private_key = generatePrivateKey(public_key, totient)
	print("Public key: ", public_key)
	print("Private key: ", private_key)
	enc_list = []
	decrypted_mess = ""
	
	for char in message:
		mess = ord(char)
		enc_mess = str(pow(mess, public_key, n))
		enc_list.append(enc_mess)

	print("Cipher Text : ", enc_mess)
	
	for enc_mess in enc_list:
		decr = (pow(int(enc_mess), private_key, n))
		decrypted_mess += chr(decr)
		
	print("Decrypted Text: ", decrypted_mess)

def runRSA(bits):
	p = genLargePrimes.generate_prime_number(bits)
	q = genLargePrimes.generate_prime_number(bits)
	n = p*q
	totient = (p-1)*(q-1)
	public_key = generatePublicKey(totient)
	private_key = generatePrivateKey(public_key, totient)
	print("Prime numbers are\np : ", p, "\nq : ", q)
	print("Modulus : ", n)
	print("Euler's Totient : ", totient)
	print("Public key: ", public_key)
	print("Private key: ", private_key)
	return n, totient, private_key, public_key


def encrypt(message, public_key, n):
	enc_list = []
	print("\nEncrypting your message\n")
	for char in message:
		mess = ord(char)
		enc_mess = str(pow(mess, public_key, n))
		print(enc_mess)
		enc_list.append(enc_mess)
	return enc_list, enc_mess

def decrypt(ct_list, ct, private_key, n):
	decrypted_mess = ""
	print("\nDecrypting your message\n")
	for ct in ct_list:
		decr = (pow(int(ct), private_key, n))
		print(decr)
		decrypted_mess += chr(decr)
		
	return decrypted_mess


# if __name__ == '__main__':
# 	bits = int(input("Enter bits: "))
# 	n, totient, private_key, public_key = runRSA(bits)
# 	message = input("Enter message: ")
# 	ct_list, ct = encrypt(message, public_key, n)
# 	print("Cipher Text: ", ct)
# 	pt = decrypt(ct_list, ct, private_key, n)
# 	print("Plain Text: ", pt)

