#!/usr/bin/env python
import os
import binascii
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

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

def showData():
	with open(file, "rb") as f:
		bytes = bytearray(f.read())

	for bits in bytes:
		temp = decimalToBinary(bits)
		print temp

	#Write bites back into file.
	#with open("tux1.bmp", "w") as w:
	#	w.write(bytes)

def hideData():
	binaryDataSize, binaryDataList = fileToBinary("text.txt")
	#Create an image object with the user selected image.
	imageObj = Image.open("butterfly.bmp")
	#Get the dimensions of the image to create a new canvas with the same dimensions
	canvasWidth, canvasHeight = imageObj.size
	#print "Canvas width: %d" %canvasWidth + " canvas height: %d" %canvasHeight
	#Convert the type of image to an RGB image.
	rgb_image = imageObj.convert('RGB')

	#r, g, b, a = rgb_image.getpixel((x,y))

	binaryConvertCounter = 0

	#print binaryDataList
	#print "Size of binary data list: %d" %binaryDataSize

	#Initial for loop to go through all the pixels in the image and get the original RGB values.
	for xWidth in range(canvasWidth):
		for yHeight in range(canvasHeight):
			r, g, b = rgb_image.getpixel((xWidth, yHeight))
			
			redDecimal = r
			greenDecimal = g
			blueDecimal = b

			redList = []
			blueList = []
			greenList = []
			rgbList = []
			rgbDecimalList = []
			tempList = []

			rgbDecimalList.append(redDecimal)
			rgbDecimalList.append(greenDecimal)
			rgbDecimalList.append(blueDecimal)

			#Convert the decimal values of RGB to binary values in a list.
			tempList = decimalToBinary(rgbDecimalList[(0)])
			for num in tempList:
				redList.append(num)
			tempList = decimalToBinary(rgbDecimalList[(1)])
			for num in tempList:
				greenList.append(num)
			tempList = decimalToBinary(rgbDecimalList[(2)])
			for num in tempList:
				blueList.append(num)

			#Create a list of lists containing the RGB binary values
			rgbList.append(redList)
			rgbList.append(greenList)
			rgbList.append(blueList)

			for i in range(3):
				#Subtract one from the binaryDataSize because it starts count at 1 not 0
				#Which the lists we will be using alongside binaryConverCounter and binaryDataSize does.
				if (binaryConvertCounter >= (binaryDataSize-1)):
					rgb_image.putpixel((xWidth,yHeight), (redDecimal, greenDecimal, blueDecimal))
					rgb_image.save("germany.bmp")
					return

				#Change the last bit in the RGB value with the data bit
				rgbList[(i)][7] = binaryDataList[binaryConvertCounter]
				#Update the RGB list with the newly changed last bit
				rgbList[(i)] = rgbList[(i)]
				#Update 
				binaryConvertCounter += 1

				#Depending on the number (0-red,1-green,2-blue)
				if (i == 0):
					redTemp = "".join(rgbList[i])
					redDecimal = binaryToDecimal(redTemp)
				elif (i == 1):
					greenTemp = "".join(rgbList[i])
					greenDecimal = binaryToDecimal(greenTemp)
				else:
					blueTemp = "".join(rgbList[i])
					blueDecimal = binaryToDecimal(blueTemp)

			rgb_image.putpixel((xWidth,yHeight), (redDecimal, greenDecimal, blueDecimal))

	rgb_image.save("germany.bmp")

if __name__ == "__main__":
	hideData()