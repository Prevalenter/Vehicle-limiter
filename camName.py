from VideoCapture import Device

def getDevName():
	namelst = []
	sign = 1
	i = -1
	while sign:
		try:
			i+=1
			cam = Device(i)
			namelst.append(cam.getDisplayName())
		except:
			sign = 0
	return namelst

if __name__ == '__main__':
	print(getDevName())