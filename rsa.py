from basics import *

# Generar RSA clave publica y privada
def gen_rsa_keys(p, q, log=False):
	assert p > 2 and q > 2
	assert mcd(p, q) == 1
	assert is_prime(p)
	assert is_prime(q)
	N = p * q
	if log:
		print("N = p * q = {} * {} = {}".format(p,q,N))
	phi_n = (p-1) * (q-1)
	if log:
		print("Phi(N) = (p-1) * (q-1) = {} * {} = {}".format(p-1, q-1, phi_n))
	# elegir RSA-exponent e
	# 1 < e < phi_n
	# mcd(e, phi_n) = 1
	e = None
	i = 0
	while not e:
		r = randint(2, phi_n)
		if mcd(r, phi_n) == 1:
			d = inverso_multiplicativo(r, phi_n, log=log)
			if d > 0:
				e = r
				if log:
					print("e = {}".format(e))
					break
		i += 1
		assert i <= phi_n

	if log:
		print("d = {}".format(d))
	return e, N, d


# cifrar mensaje con RSA clave publica
def cifrar_rsa(m, e, N):
	c = (m ** e) % N
	return c


# descifrar mensaje con RSA clave privada
def descifrar_rsa(c, d, N):
	m = (c ** d) % N
	return m




# print(algoritmo_extendido_euclides(164, 28, log=True))
# print(inverso_multiplicativo(3, 8))
#print(gen_rsa_keys(7, 11))

e, N, d = gen_rsa_keys(17, 23, log=True)
c = cifrar_rsa(9, e, N)
print(c)
m = descifrar_rsa(c, d, N)
print(m)