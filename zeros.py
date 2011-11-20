
r = lambda x: x % 1410000017  # round by modulo

def Z9(l):
	""" 
		Calculate zeros from 0 to l nines, without counting leading zeros
		Z9(2) = number_of_zeros("99")
		Z9(3) = number_of_zeros("999")

	"""
	if l <= 1: return 1
	ll = l - 1
	zl = 9 * ll * (10 ** (ll-1))
	zll = Z9(ll)
	# print "l=%d\t zl=%d, zll=%d" % (l, zl, zll)
	return r(zl + zll)

def zeros_part(k,l):
	""" zeros (without leading) from "k-1 9 9 9 9 9 9" (l nines) to 0 
		k-1 9 9 9 9 9 9
		 .  
		 .
		 .
		 1  0 0 0 0 0 0 
		    9 9 9 9 9 9
		  		      .
		  		      .
		  		      .
		  		  	  0
	"""
	assert k > 0
	s = (k-1) * l * 10 ** (l-1) if l else 0
	z9 = Z9(l)
	return r(z9 + s)

def zeros_leading(S):
	""" Calculate including leading zeros """
	if not S: return 0
	k = int(S[0])
	l = len(S)-1
	if k == 0:
		s = int(S[1:] or 0) + 1
	else:
		s = k * l * (10 ** (l-1)) + 10 ** l if l else 1
	#print "[%s] %dx%d-> %d" % (S, k, l, s)
	return r(s + zeros_leading(S[1:]))

def number_of_zeros(S):
	#return direct(S)
	l = len(S)-1
	#print '>>> ', S
	part = zeros_part(int(S[0]), l)
	full =  zeros_leading(S[1:])
	#print "S = ", part+full, " part=", part, " full=", full
	return part + full
	

def direct(S):
	""" dummy algorithm """
	N = int(S)
	zeros = lambda i: sum( 1 if c=='0' else 0 for c in str(i))
	return sum(zeros(i) for i in xrange(N+1))

if __name__ == "__main__":
	assert Z9(0) == 1
	assert Z9(1) == 1 
	assert Z9(2) == 10
	assert Z9(3) == 190
	assert Z9(4) == 2890

	assert zeros_leading("0") == 1
	assert zeros_leading("1") == 1
	assert zeros_leading("2") == 1
	assert zeros_leading("9") == 1
	assert zeros_leading("00") == 2
	assert zeros_leading("01") == 3
	assert zeros_leading("02") == 4
	assert zeros_leading("03") == 5
	assert zeros_leading("04") == 6
	assert zeros_leading("10") == 12
	assert zeros_leading("11") == 12
	assert zeros_leading("12") == 12
	assert zeros_leading("13") == 12
	assert zeros_leading("20") == 13
	assert zeros_leading("21") == 13
	assert zeros_leading("22") == 13
	assert zeros_leading("99") == 20


	assert number_of_zeros("1") == 1
	assert number_of_zeros("2") == 1
	assert number_of_zeros("3") == 1
	assert number_of_zeros("10") == 2
	assert number_of_zeros("11") == 2
	assert number_of_zeros("12") == 2
	assert number_of_zeros("20") == 3
	assert number_of_zeros("21") == 3
	assert number_of_zeros("22") == 3
	assert number_of_zeros("90") == 10
	assert number_of_zeros("100") == 12
	assert number_of_zeros("101") == 13
	assert number_of_zeros("103") == 15
	assert number_of_zeros("104") == 16
	assert number_of_zeros("105") == 17
	assert number_of_zeros("106") == 18
	assert number_of_zeros("107") == 19
	assert number_of_zeros("108") == 20
	assert number_of_zeros("109") == 21
	assert number_of_zeros("110") == 22
	assert number_of_zeros("200") == 32
	assert number_of_zeros("201") == 33
	assert number_of_zeros("219") == 42
	assert number_of_zeros("9") == 1
	assert number_of_zeros("99") == 10
	assert number_of_zeros("999") == 190
	assert number_of_zeros("9999") == 2890
	assert number_of_zeros("54321") == 21263
	assert number_of_zeros("54331") == 21264
	print "Tests PASSED"
 
 	print number_of_zeros("5032122554650699999999999989898787987987987989898985")

 	import timeit
 	t = timeit.Timer("""
		number_of_zeros("1234567890"*10)
	""", "from zeros import number_of_zeros")
	print "t =", t.timeit(10)