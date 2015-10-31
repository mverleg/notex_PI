

def version_str2intrest(txt, mx = 10000):
	if txt.count('.') == 0:
		major, minor, rest = '0' + txt, 0, ''
	elif txt.count('.') == 1:
		(major, minor), rest = txt.split('.'), ''
	else:
		major, minor, rest = txt.split('.', maxsplit = 2)
	major, minor = int(major), int(minor)
	assert major < mx - 1 and minor < mx - 1
	return mx * major + minor, rest


def version_intrest2str(nr, rest, mx = 10000):
	return '{0:d}.{1:d}'.format(nr // mx, nr % mx) + ('.{0:s}'.format(rest) if rest else '')


def version_int2str(nr, mx = 10000):
	return '{0:d}.{1:d}'.format(nr // mx, nr % mx)


def version_str2int(txt, mx = 10000):
	return version_str2intrest(txt)[0]


def version_getmax(mx = 10000):
	return mx * mx + mx


