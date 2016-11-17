from random import randint

# Basic methods

# algoritmo de euclides para obtener el maximo comun divisor mcd de dos enteros
def mcd(a, b):
    while b>0:
        r = a%b
        a = b
        b = r
    return a

# minimo comun multiplo mcm
# mcd(a,b) * mcm(a,b) = a*b
# mcm(a,b) = a*b/mcd(a,b)
def mcm(a,b):
    return a*b/mcd(a,b)


# algoritmo extendido euclido
def algoritmo_extendido_euclides(a_, b_, log=False):
	a = [a_]
	b = [b_]
	q = [a_/b_]
	r = [a_%b_]
	x = []
	y = []
	i = 1
	while r[-1] > 0:
		a.append(b[-1])
		b.append(r[-1])
		q.append(a[-1]/b[-1])
		r.append(a[-1]%b[-1])
		i += 1
	d = b[-1]
	x.append(0)
	y.append(1)
	i -= 1
	while i > 0:
		x.append(y[-1])
		y.append(x[-2] - (y[-1] * q[i-1]))

		i -= 1
	x.reverse()
	y.reverse()
	if log:
		print("a\tb\tq\tr\tx\ty")
		print("-"*80)
		for i in range(len(x)):
			print("{}\t{}\t{}\t{}\t{}\t{}".format(a[i], b[i], q[i], r[i], x[i], y[i]))

	return (d, x[0], y[0])


# Usar la igualidad de Bezout para calcular d = e^-1 mod n
# d * e + k * n = mcd(e, n) = 1
def inverso_multiplicativo(e, n, log=False):
	mcd, d, k = algoritmo_extendido_euclides(e, n, log=log)
	assert mcd == 1
	if log:
		print("{} * {} + {} * {} = {} ".format(d,e,k,n, (d*e + k*n)))
	return d


# prime test
def is_prime(n):
	x = (n/2)+1
	t = 2
	while t <= x:
		if n%t == 0:
			return False
		t += 1
	return True
