'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  SOURCE FILE:    steganographyEncode.py
--
--  PROGRAM:        Hides selected data into an image using the basic LSB steganography method.
--
--  FUNCTIONS:      usage(), 
--                  decimalToBinary(decimal), 
--                  binaryToDecimal(binary), 
--                  asciiToBinary(string),
--					binaryToAscii(binaryData),
--					fileToBinary(file),
--					compareFileSize(coverFile, dataFile, headerSize),
--					dataLSB(rgb_image, binaryDataSize, binaryDataList, canvasWidth, canvasHeight),
--					hideData().
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
	if (len(sys.argv) != 4):
		print "Usage (Make sure to include file extensions): " + sys.argv[0] + " -CoverImage " + "-Data " + "-OutputName"
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
--  Name:       fileToBinary
--  Parameters:
--      file
--        Path of the selected file.
--  Return Values:
--      fileName
--			The name of the selected file.
--      binaryDataSize
--			The size of the selected data (how many binary bits)
--      binaryDataList
--			The list of all the binary data values.
--  Description:
--      Function to take the passed in file, read the file and convert it to binary bits as well as
--		returning the filename and file size (in bits).
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def fileToBinary(file):
	fileName = file
	binaryDataList = []
	binaryBitsList = []
	binaryDataString = ""

	#Open the file and conver the data to bytes
	with open(fileName, "rb") as f:
		bytes = bytearray(f.read())

	#For each byte, convert it to binary and concatenate it to a string variable.
	for bits in bytes:
		binaryDataString += bin(bits)[2:].zfill(8)

	for char in binaryDataString:
		binaryDataList.append(char)
	
	#print binaryDataList

	#Get the length of the data string in order to know when to stop iterating later.
	binaryDataSize = len(binaryDataString)

	return fileName, binaryDataSize, binaryDataList

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       compareFileSize
--  Parameters:
--      coverFile
--        Path of the cover file
--      dataFile
--        Path of the data file
--      headerSize
--        The size of the header (filename, extension and datasize)
--  Return Values:
--      0
--			Essentially a flag checker - 0 meaning can't fit the data in the image.
--      1
--			Essentially a flag checker - 1 meaning can fit the data in the image.
--      binaryDataList
--			The list of all the binary data values.
--  Description:
--      Function to compare the cover image size to the datafile plus the header size to calculate
--		if the data can be stored in the selected bitmap image.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
#Comparison method to determine if the data file can fit inside the cover image.
def compareFileSize(coverFile, dataFile, headerSize):
	coverImage = Image.open(coverFile)
	width, height = coverImage.size
	#Image's width x height x 3 (3 bits per pixel)
	coverFileSize = width * height * 3
	#Returns the file size in bytes
	dataFileSize = os.path.getsize(dataFile)
	#Multiply the dataFileSize by 8 since there are 8 bits in a byte.
	dataFileSize *= 8
	#Actual comparison after all calculations are done.
	if (coverFileSize >= (dataFileSize + headerSize)):
		return 1
	else:
		return 0

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       dataLSB
--  Parameters:
--      rgb_image
--        The image object that has been turned to RGB mode.
--      binaryDataSize
--        The size of the data file.
--      binaryDataList
--        The list containing all the binary data bits.
--      canvasWidth
--        The width of the cover image.
--      canvasHeight
--        The heigh of the cover image.
--  Return Values:
--		None
--  Description:
--      Main module function that will be used for hiding the data and header in the image through manipulating
--		the LSB of the image's RGB pixel values.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def dataLSB(rgb_image, binaryDataSize, binaryDataList, canvasWidth, canvasHeight):
	binaryConvertCounter = 0
	#Initial for loop to go through all the pixels in the image and get the original RGB values.
	for xWidth in range(canvasWidth):
		for yHeight in range(canvasHeight):
			r, g, b = rgb_image.getpixel((xWidth, yHeight))
			
			#Instantiate the original pixel RGB values in order later reference them if the LSBs are not changed in the RGB value.
			redDecimal = r
			greenDecimal = g
			blueDecimal = b

			#Clear the previous values of the lists - re-instantiate an empty list.
			redList = []
			blueList = []
			greenList = []
			rgbList = []
			rgbDecimalList = []
			tempList = []

			#Create a list of RGB values in decimal to later iterate through.
			rgbDecimalList.append(redDecimal)
			rgbDecimalList.append(greenDecimal)
			rgbDecimalList.append(blueDecimal)

			#Convert the decimal values of all RGB to binary values in a list.
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
				#Which the lists we will be using alongside binaryConverCounter and binaryDataSize does.
				#If the binaryConvertCounter is larger than the size of the binary data, it means it doesn't
				#divide into 3 evenly, and therefore will have one or two values (green and/or blue) that will not
				#have their LSB changed, therefore assign them to the original pixel value.
				if (binaryConvertCounter >= binaryDataSize):
					rgb_image.putpixel((xWidth,yHeight), (redDecimal, greenDecimal, blueDecimal))
					#If the binary data stream does not go into 3 bits (RGB) exactly, then use this to save the photo
					rgb_image.save(str(sys.argv[3]))
					print "Data successfully hidden in image. Output image: \'stegoImage.bmp\'"
					return

				#Change the last bit in the RGB value with the data bit
				rgbList[(i)][7] = binaryDataList[binaryConvertCounter]
				#Update the RGB list with the newly changed last bit
				rgbList[(i)] = rgbList[(i)]
				#Increment counter 
				binaryConvertCounter += 1

				#Depending on the number (0-red,1-green,2-blue), change the binary list back to decimal value
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
	#Only if the bits go evenly into 3 (RGB), then it will get here and then return.
	rgb_image.save(str(sys.argv[3]))
	print "Data successfully hidden in image. Output image: \'stegoImage.bmp\'"
	return

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
--  FUNCTION
--  Name:       hideData
--  Parameters:
--		None
--  Return Values:
--		None
--  Description:
--      Function to prep the "artificial" header for the image which will contain the 
-- 		filename, extension and data size. As well as checking that the image is large enough
--		to hide the data and that the cover image is a bitmap format.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''  
def hideData():
	#Get the name, size of the whole binary data string as well as the list 
	#of the binary data itself from the selected file.
	fileName, binaryDataSize, binaryDataList = fileToBinary(str(sys.argv[2]))
	#Create an image object with the user selected image.
	imageObj = Image.open(str(sys.argv[1]))
	#Get the dimensions of the image to create a new canvas with the same dimensions
	canvasWidth, canvasHeight = imageObj.size
	#print "Canvas width: %d" %canvasWidth + " canvas height: %d" %canvasHeight
	#Convert the type of image to an RGB image.
	rgb_image = imageObj.convert('RGB')

	headerFlag = 0
	headerNameFlag = 0
	headerSizeFlag = 0
	fileNameList = []
	fileSizeList = []
	totalDataList = []

	nullCharacter = '\0'
	nullCharacter = asciiToBinary(nullCharacter)

	#Filling the header data first with the filename and filesize before the actual data is hidden.
	while (headerFlag == 0):
		if (headerNameFlag == 0):
			fileNameBinary = asciiToBinary(fileName)
			for i in fileNameBinary:
				fileNameList.append(i)
			#Add a null character delimiter in order to help separate filename, filesize and data bits.
			for i in nullCharacter:
				fileNameList.append(i)
			#Add 8 to it in order to compensate for adding a null character terminator
			fileNameSize = (len(fileNameBinary) + 8)
			headerNameFlag = 1
		if (headerSizeFlag == 0):
			#Change the data size from int to string in order to do the ASCII convert
			fileSizeBinary = asciiToBinary(str(binaryDataSize))
			for i in fileSizeBinary:
				fileSizeList.append(i)
			for i in nullCharacter:
				fileSizeList.append(i)
			#Add 8 to it in order to compensate for adding a null character terminator
			fileSizeSize = (len(fileSizeBinary) + 8)
			headerSizeFlag = 1
		if (headerNameFlag == 1 and headerSizeFlag == 1):
			headerFlag = 1
	#Alternative would be len(totalDataList)
	headerSize = fileNameSize + fileSizeSize
	totalDataSize = fileNameSize + fileSizeSize + binaryDataSize	
	totalDataList.extend(fileNameList)
	totalDataList.extend(fileSizeList)
	totalDataList.extend(binaryDataList)

	fileExtCheck = fileName.split(".")
	fileFormat = fileExtCheck[len(fileExtCheck)-1]

	if (fileFormat != "bmp"):
		print "The cover image must be a bitmap file. Please try again."
		sys.exit()

	comparisonResult = compareFileSize(str(sys.argv[1]), str(sys.argv[2]), headerSize)
	if (comparisonResult == 1):
		#Hide the actual data using the RGB_Image, with size of the data, binary list of the data, rgb_image's heigh and width starting at position where file size ended.
		dataLSB(rgb_image, totalDataSize, totalDataList, canvasWidth, canvasHeight)
	else:
		print "The cover image is too small to store the selected data. Please try again."
		sys.exit()

if __name__ == "__main__":
	usage()
	hideData()