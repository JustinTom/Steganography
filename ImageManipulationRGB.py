#!/usr/bin/env python
import os
import binascii
from PIL import Image

def asciiToBinary(textData):
	#binaryData = bin(int(binascii.hexlify(textData), 16))
	binaryData = ''.join(format(letter,'b').zfill(8) for letter in bytearray(textData))
	return binaryData

def binaryToAscii(binaryData):
	tempData = int(binaryData, 2)
	stringData = binascii.unhexlify('%x' % tempData)
	return stringData

def decimalToBinary(decimal):
	binaryValue = bin(decimal)[2:].zfill(8)
	return binaryValue

def binaryToDecimal(binary):
	#Convert binary to decimal
	decimalValue = int(binary, 2)
	return decimalValue

def fileToBinary(file):
	binaryDataList = []
	binaryBitsList = []
	binaryDataString = ""

	#Open the file and conver the data to bytes
	with open(file, "rb") as f:
		bytes = bytearray(f.read())

	#For each byte, convert it to binary and concatenate it to a string variable.
	for bits in bytes:
		binaryDataString += bin(bits)[2:].zfill(8)

	for char in binaryDataString:
		binaryDataList.append(char)
	
	#print binaryDataList

	#Get the length of the data string in order to know when to stop iterating later.
	binaryDataSize = len(binaryDataString)

	return binaryDataSize, binaryDataList

def binaryToFile():
	#tux1.bmp is the new file name
	with open("tux1.bmp", "w") as w:
		w.write(bytes)

#Code method to compare the file sizes - 3/8 ratio?
def compareFileSize(coverFile, dataFile):
	coverFileSize = os.path.getsize(coverFile)
	print "Cover File Size (Bytes): %d"  %coverFileSize
	dataFileSize = os.path.getsize(dataFile)
	print "Data File Size (Bytes): %d" %dataFileSize
	#Storing LSB in RGB only allows 3 bits, therefore per byte (8 bits).
	#3/8 is the ratio you are able to store files in the original image.
	#I also subtract 250 bits from the result for header space.
	if (((dataFileSize/coverFileSize)-250) <= (3/8)):
		return 1
	else:
		return 0

def hideData():
	binaryDataSize, binaryDataList = fileToBinary("text.txt")
	#Create an image object with the user selected image.
	imageObj = Image.open("butterfly.bmp")
	imageObjNew = imageObj.copy()
	#Get the dimensions of the image to create a new canvas with the same dimensions
	canvasWidth, canvasHeight = imageObjNew.size
	#print "Canvas width: %d" %canvasWidth + " canvas height: %d" %canvasHeight
	#Convert the type of image to an RGB image.
	rgb_img = imageObjNew.convert('RGB')

	#r, g, b, a = rgb_img.getpixel((x,y))

	binaryConvertCounter = 0
	redList = []
	blueList = []
	greenList = []

	print binaryDataList
	print "Size of binary data list: %d" %binaryDataSize

	for xWidth in range(canvasWidth):
		for yHeight in range(canvasHeight):
			r, g, b = rgb_img.getpixel((xWidth, yHeight))
			print "original %d, %d, %d" %(r, g, b)

			if ((binaryDataSize - binaryConvertCounter) >= 3):
				#Constant checker to see if the binary counter is smaller than the total size of the binary data
				#Checker is only for smaller than since the increment is after checker
				if binaryConvertCounter < binaryDataSize:
					redBinary = decimalToBinary(r)
					redList = list(redBinary)
					#Hard code the array position to be 7 since the size of the decimal value will always be 8
					#If not you can use (redList.length-1)
					redList[7] = binaryDataList[binaryConvertCounter]
					binaryConvertCounter += 1
					#Replace the old binary with the new one with the LSB changed.
					redBinary = "".join(redList)
					redDecimal = binaryToDecimal(redBinary)
				else:
					print "I'M MR MEESEEKS LOOK AT ME!"
					#Should take the filename from header and place as new filename
					rgb_img.save("tempFileName.bmp",format="bmp")
					return

				if binaryConvertCounter < binaryDataSize:
					greenBinary = decimalToBinary(g)
					greenList = list(greenBinary)
					greenList[7] = binaryDataList[binaryConvertCounter]
					binaryConvertCounter += 1
					greenBinary = "".join(greenList)
					greenDecimal = binaryToDecimal(greenBinary)
				else:
					print "I'M MR MEESEEKS LOOK AT ME!!"
					return

				if binaryConvertCounter < binaryDataSize:
					blueBinary = decimalToBinary(b)
					blueList = list(blueBinary)
					blueList[7] = binaryDataList[binaryConvertCounter]
					binaryConvertCounter += 1
					blueBinary = "".join(blueList)
					blueDecimal = binaryToDecimal(greenBinary)
				else:
					print "I'M MR MEESEEKS LOOK AT ME!!!"
					return

				#Put the new pixel in place of the old one with the new altered binary RGB values
				#print "New %d, %d, %d " %(redDecimal, greenDecimal, blueDecimal)
				rgb_img.putpixel((xWidth, yHeight),(0, 0, 255, 100))
			
			#Else if there is less than 3 bits left from the data --> 2, only change the red and green values.
			elif ((binaryDataSize - binaryConvertCounter) == 2):
				#Change the LSB of the red pixel value.
				redBinary = decimalToBinary(r)
				redList = list(redBinary)
				#Hard code the array position to be 7 since the size of the decimal value will always be 8
				#If not you can use (redList.length-1)
				redList[7] = binaryDataList[binaryConvertCounter]
				binaryConvertCounter += 1
				#Replace the old binary with the new one with the LSB changed.
				redBinary = "".join(redList)
				redDecimal = binaryToDecimal(redBinary)
				
				#Change the LSB of the blue pixel value.
				greenBinary = decimalToBinary(g)
				greenList = list(greenBinary)
				greenList[7] = binaryDataList[binaryConvertCounter]
				binaryConvertCounter += 1
				greenBinary = "".join(greenList)
				greenDecimal = binaryToDecimal(greenBinary)

				rgb_img.putpixel((xWidth, yHeight),(redDecimal, greenDecimal, b))

				return

			#Else there is only 1 bit left from the data, only change the red value.
			else:
				#Change the LSB of the red pixel value.
				redBinary = decimalToBinary(r)
				redList = list(redBinary)
				#Hard code the array position to be 7 since the size of the decimal value will always be 8
				#If not you can use (redList.length-1)
				print binaryConvertCounter
				redList[7] = binaryDataList[binaryConvertCounter]
				binaryConvertCounter += 1
				#Replace the old binary with the new one with the LSB changed.
				redBinary = "".join(redList)
				redDecimal = binaryToDecimal(redBinary)

				rgb_img.putpixel((xWidth, yHeight),(redDecimal, g, b))

				return


if __name__ == "__main__":
	hideData()