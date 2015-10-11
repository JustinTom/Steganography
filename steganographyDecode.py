'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    steganographyDecode.py
--
--  PROGRAM:        Reveals the data hidden in the stego image.
--
--  FUNCTIONS:      usage(), 
--                  decimalToBinary(decimal), 
--                  binaryToDecimal(binary), 
--                  asciiToBinary(string),
--					binaryToAscii(binaryData),
--					showData().
--
--  DATE:           September 28, 2015
--
--  REVISIONS:      October 5, 2015
--
--  NOTES:
--  The program requires "Pillow"/"PIL", an image manipulation library for Python.
--  https://github.com/python-pillow/Pillow
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#!/usr/bin/env python
import os, binascii, array, sys
from PIL import Image

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       usage
--  Parameters:
--      None
--  Return Values:
--      None
--  Description:
--      Function to ensure there are enough arguments to properly run the program
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def usage():
	if (len(sys.argv) != 2):
		print "Usage (Make sure to include file extensions): " + sys.argv[0] + " -StegoImage"
		sys.exit()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       decimalToBinary
--  Parameters:
--      decimal
--        The decimal value of a number or character(s)
--  Return Values:
--      binaryValue
--  Description:
--      Function to take the passed in decimal parameter, convert it and return the respective binary value.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def decimalToBinary(decimal):
	#Removes the preceeding '0b' identifier from the decimal conversion to binary
	#and keeps the value at 8 characters (zfill), keeping the leading zeros.
	binaryValue = bin(decimal)[2:].zfill(8)
	return binaryValue

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       binaryToDecimal
--  Parameters:
--      binary
--        The binary value of a number or character(s)
--  Return Values:
--      decimalValue
--  Description:
--      Function to take the passed in binary parameter, convert it and return the respective decimal value.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def binaryToDecimal(binary):
	#Convert binary to decimal
	decimalValue = int(binary, 2)
	#Returns an integer decimal value.
	return decimalValue

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       asciiToBinary
--  Parameters:
--      string
--        The string of characters in ascii format
--  Return Values:
--      binaryString
--  Description:
--      Function to take the passed in string characters and convert them to binary.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def asciiToBinary(string):
	binaryString = ''.join(format(letter,'b').zfill(8) for letter in bytearray(string))
	return binaryString

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       binaryToAscii
--  Parameters:
--      binaryData
--        A string if binary values.
--  Return Values:
--      stringData
--  Description:
--      Function to take the passed in a string of binary values and convert them to ascii format.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def binaryToAscii(binaryData):
	tempData = int(binaryData, 2)
	stringData = binascii.unhexlify('%x' % tempData)
	return stringData

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       showData
--  Parameters:
--      None
--  Return Values:
--		None
--  Description:
--      Main module function to extract the data from the steganography image from the encoder program.
--		Will go through the "header" and extract the file name, extension and data size as well as the data itself
--		and re-construct it to a file matching the original data. The output will be placed in the "decodedFiles" directory.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def showData():
	stegoImg = Image.open(str(sys.argv[1]))
	stegoImg = stegoImg.convert('RGB')
	imgWidth, imgHeight = stegoImg.size
	byte = ""
	byteList = []
	byteString = ""
	nullTerminator = "00000000"
	nameFlag = 0
	sizeFlag = 0

	dataIndex = 0
	dataBitStream = ""
	dataByteStream = []

	for xWidth in range(imgWidth):
		for yHeight in range(imgHeight):
			r, g, b = stegoImg.getpixel((xWidth,yHeight))

			rLSB = (decimalToBinary(r)[-1])
			gLSB = (decimalToBinary(g)[-1])
			bLSB = (decimalToBinary(b)[-1])

			rgbLSBList = [rLSB, gLSB, bLSB]

			#Loop 3 times (RGB) and use their LSB accordingly.
			for i in range(3):
				#Create a string of the LSBs
				byte += rgbLSBList[i]
				#For every 8 bits (a single byte), do the checks.
				if len(byte) == 8:
					byteList.append(byte)
					#If you haven't gotten the filename yet..
					if (nameFlag == 0):
						#If the byte is a null terminator character (the delimiter)
						if (byte == nullTerminator):
							for item in byteList:
								byteString += item
							#Remove the last 8 bits (delimiter's null character)
							byteString = byteString[:-8]
							#Convert the binary to ascii.
							fileName = binaryToAscii(byteString)
							#Now that we got the file name, we can flip the checker flag and erase the data to prevent
							#it from being read as the main data stream.
							nameFlag = 1
							byteList = []
							byteString = ""
					elif (sizeFlag == 0):
						if (byte == nullTerminator):
							for item in byteList:
								byteString += item
							byteString = byteString[:-8]
							fileSize = int(binaryToAscii(byteString))
							sizeFlag = 1
							byteList = []
							byteString = ""
							#Continue out of the if loop after the header fields are extracted (name and size)
							continue
					#Clear and reset the byte string to be used again at the loop.
					byte = ""

				if (nameFlag == 1 and sizeFlag == 1):
					#As long as the data index is smaller than the size of the total data..
					if (dataIndex < fileSize):
						dataBitStream += rgbLSBList[i]
						dataIndex += 1

	#Convert the bit stream to a byte stream, divide the size of the data by 8
	#since we are now converting the bits to bytes (8:1). This will also help cut out
	#any of the extra "original" LSB RGB values that we took from the loop which does not
	#contain any of the "real" data we want.
	for i in range(fileSize/8):
		#Appends every 8 bits to the dataByteStream list, changing it back to a byte.
		#Changes the value from binary to decimal
		dataByteStream.append(binaryToDecimal(dataBitStream[i*8:(i+1)*8]))
	fileDataBytes = bytearray(dataByteStream)

	#Separate the file name and extension (in case for later use)
	fileName, fileExt = fileName.split('.')
	#Output file name and extension
	outputFileName = "Output_" + fileName + "." + fileExt
	#Outputs the decoded file to the decodedFiles directory
	with open("decodedFiles/" + outputFileName, "wa") as w:
		w.write(fileDataBytes)
	print "Image successfully decoded and saved as " + outputFileName + " in \'decodedFiles\' directory"

if __name__ == "__main__":
	usage()
	showData()