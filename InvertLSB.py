# coding: utf-8

# Image Steganography with Invert LSB
# Invert LSB is a less lossy version of LSB
# LSB requires flipping the LS bits, hence loss of data
# In traditional LSB, as many LSB are flipped as needed to contain the secret message
# In invert LSB, only a fraction of those bits should be flipped
# The bits to invert are chosen based on its 2nd and 3rd LSB (of the same byte)
# If bit x's 2nd and 3rd LSB have more CHANGED than UNCHANGED, bit x is double-flipped
# (so there's now more UNCHANGED than CHANGED)
# This "flip Unchanged/Changed" data are kept in a dictionary

# NOTE: Use a big image!!

# Credit: Rupali Roy, https://towardsdatascience.com/hiding-data-in-an-image-image-steganography-using-python-e491b68b1372
# This InvertLSB.py file was written based on the traditional LSB from Rupali
# As mentioned, Invert LSB is a modified and more efficient version of traditional LSB
# From our team, big thanks to you, Rupali



#import all the required libraries
import cv2
import numpy as np
from collections import defaultdict
import types
#from google.colab.patches import cv2_imshow #Google colab crashes if you try to display
#image using cv2.imshow() thus use this import


def messageToBinary(message):
  if type(message) == str:
    return ''.join([ format(ord(i), "08b") for i in message ])
  elif type(message) == bytes or type(message) == np.ndarray:
    return [ format(i, "08b") for i in message ]
  elif type(message) == int or type(message) == np.uint8:
    return format(message, "08b")
  else:
    raise TypeError("Input type not supported")



# Function to hide the secret message into the image

def hideData(image, secret_message):

  # calculate the maximum bytes to encode
  n_bytes = image.shape[0] * image.shape[1] * 3 // 8
  print("Maximum bytes to encode:", n_bytes)

  #Check if the number of bytes to encode is less than the maximum bytes in the image
  if len(secret_message) > n_bytes:
      raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")
  
  secret_message += "#####" # you can use any string as the delimeter

  data_index = 0
  # convert input data to binary format using messageToBinary() fucntion
  binary_secret_msg = messageToBinary(secret_message)
  print('Message: ', binary_secret_msg)
  print('Message Length: ', len(binary_secret_msg))

  # Dict to keep track of flipped bits based on permutations of 2nd and 3rd LSB
  # k,v Example is 01: [10, 20]
  # 01, 0 is the 3rd, 1 is the 2nd LSB
  # 10 is the amount of times the permu have been considered AND CHANGED
  # 20 is the amount of times the permu have been considered AND NOT CHANGED
  doubleDict = {
      '00': [0, 0],
      '01': [0, 0],
      '10': [0, 0],
      '11': [0, 0]
  }

  data_len = len(binary_secret_msg) #Find the length of data that needs to be hidden
  for values in image:
      for pixel in values:
          print('PIXEL: ', pixel)
          # convert RGB values to binary format
          r, g, b = messageToBinary(pixel)
          print(f'Red: {r}, Green: {g}, Blue: {b}')
          # modify the least significant bit only if there is still data to store
          if data_index < data_len:
              # hide the data into least significant bit of red pixel
              print('Binary Converter RED: ', r[:-1] + binary_secret_msg[data_index])

              # If considered AND CHANGED, or: current LSB != current msg bit
              if r[-1:] != binary_secret_msg[data_index]:
                  doubleDict[str(r[-3:-1])][0] += 1
              # If considered AND NOT CHANGED, or: current LSB == current msg bit
              else:
                  doubleDict[str(r[-3:-1])][1] += 1

              pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          if data_index < data_len:
              # hide the data into least significant bit of green pixel
              if g[-1:] != binary_secret_msg[data_index]:
                  doubleDict[str(g[-3:-1])][0] += 1
              else:
                  doubleDict[str(g[-3:-1])][1] += 1
              pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          if data_index < data_len:
              # hide the data into least significant bit of  blue pixel
              if b[-1:] != binary_secret_msg[data_index]:
                  doubleDict[str(b[-3:-1])][0] += 1
              else:
                  doubleDict[str(b[-3:-1])][1] += 1
              pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          # if data is encoded, just break out of the loop
          if data_index >= data_len:
              break

  print(doubleDict)

  #The extract key contains which bit to invert back
  extractKey = ['0', '0', '0', '0']
  extractCount = 0
  for permu, compare in doubleDict.items():
      # if CHANGED > UNCHANGED
      # else CHANGED <= UNCHANGED
      if compare[0] > compare[1]:
          extractKey[extractCount] = '1'
      extractCount += 1
  extractKey = ''.join(extractKey)
  print('Extract: ', extractKey)
  print('Extract type ', type(extractKey))
  return image


def hideData(image, secret_message):
    # calculate the maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode:", n_bytes)

    # Check if the number of bytes to encode is less than the maximum bytes in the image
    if len(secret_message) > n_bytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")

    secret_message += "#####"  # you can use any string as the delimeter

    data_index = 0
    # convert input data to binary format using messageToBinary() fucntion
    binary_secret_msg = messageToBinary(secret_message)
    print('Message: ', binary_secret_msg)
    print('Message Length: ', len(binary_secret_msg))

    # Dict to keep track of flipped bits based on permutations of 2nd and 3rd LSB
    # k,v Example is 01: [10, 20]
    # 01, 0 is the 3rd, 1 is the 2nd LSB
    # 10 is the amount of times the permu have been considered AND CHANGED
    # 20 is the amount of times the permu have been considered AND NOT CHANGED
    doubleDict = {
        '00': [0, 0],
        '01': [0, 0],
        '10': [0, 0],
        '11': [0, 0]
    }

    data_len = len(binary_secret_msg)  # Find the length of data that needs to be hidden
    for values in image:
        for pixel in values:
            # convert RGB values to binary format
            r, g, b = messageToBinary(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # hide the data into least significant bit of red pixel
                # If considered AND CHANGED, or: current LSB != current msg bit
                if r[-1:] != binary_secret_msg[data_index]:
                    doubleDict[str(r[-3:-1])][0] += 1
                # If considered AND NOT CHANGED, or: current LSB == current msg bit
                else:
                    doubleDict[str(r[-3:-1])][1] += 1
                pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
                print('FIRST ROUND')
                print(f'Red:{pixel[0]}')
            if data_index < data_len:
                # hide the data into least significant bit of green pixel
                if g[-1:] != binary_secret_msg[data_index]:
                    doubleDict[str(g[-3:-1])][0] += 1
                else:
                    doubleDict[str(g[-3:-1])][1] += 1
                pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
                print('FIRST ROUND')
                print(f'Green:{pixel[1]}')
            if data_index < data_len:
                # hide the data into least significant bit of  blue pixel
                if b[-1:] != binary_secret_msg[data_index]:
                    doubleDict[str(b[-3:-1])][0] += 1
                else:
                    doubleDict[str(b[-3:-1])][1] += 1
                pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
                print('FIRST ROUND')
                print(f'Blue:{pixel[2]}')
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break

    data_index = 0
    # Invert data back based on doubleDict results
    # Essentially, this is a repeat of the previous subroutine for those with CHANGED > UNCHANGED
    for values in image:
        for pixel in values:
            # convert RGB values to binary format
            r, g, b = messageToBinary(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # flip the LSB of RED pixel
                # if 2nd & 3rd LSB match key of doubleDict, And (in its value) its CHANGED > UNCHANGED, then flip
                # else: do nothing
                if doubleDict[str(r[-3:-1])][0] > doubleDict[str(r[-3:-1])][1]:
                    pixel[0] = int(r[:-1] + ('1' if r[-1:] == '0' else '0'), 2)
                data_index += 1
                print('SECOND ROUND')
                print(f'Red:{pixel[0]}')
            if data_index < data_len:
                # flip the LSB of GREEN pixel
                if doubleDict[str(g[-3:-1])][0] > doubleDict[str(g[-3:-1])][1]:
                    pixel[1] = int(g[:-1] + ('1' if g[-1:] == '0' else '0'), 2)
                data_index += 1
                print('SECOND ROUND')
                print(f'Green:{pixel[1]}')
            if data_index < data_len:
                # flip the LSB of BLUE pixel
                if doubleDict[str(b[-3:-1])][0] > doubleDict[str(b[-3:-1])][1]:
                    pixel[2] = int(b[:-1] + ('1' if b[-1:] == '0' else '0'), 2)
                data_index += 1
                print('SECOND ROUND')
                print(f'Blue:{pixel[2]}')
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break

    # The extract key contains which bit to invert back
    extractKey = ['0', '0', '0', '0']
    extractCount = 0
    for permu, compare in doubleDict.items():
        # if CHANGED > UNCHANGED
        # else CHANGED <= UNCHANGED
        if compare[0] > compare[1]:
            extractKey[extractCount] = '1'
        extractCount += 1
    extractKey = ''.join(extractKey)
    print('EXTRACT: ', extractKey)
    print(f'PLEASE REMEMBER THIS EXTRACT KEY FOR THIS IMAGE!!')
    print('Extract type ', type(extractKey))
    return image


def showData(image, extractKey):
  # Make a dictionary based on the extractKey
  # Used to undo the invert to extract the correct message
  doubleDict = {
        '00': False,     #False means UNCHANGED, hence no invert undo
        '01': False,     #True means CHANGED, hence invert undo (flip LSB)
        '10': False,
        '11': False
    }
  extractCount = 0
  for permu, changed in doubleDict.items():
      # if extractKey index == 1, means CHANGED, means replace False with True
      # else: extractKey index == 0, means UNCHANGED, do nothing (since default is False)
      if extractKey[extractCount] == '1':
          doubleDict[permu] = True
      extractCount += 1
  print('Double Dict', doubleDict)

  binary_data = ""
  for values in image:
      for pixel in values:
          r, g, b = messageToBinary(pixel) #convert the red,green and blue values into binary format

          # Undo invert
          # Flip LSB if doubleDict[2nd&3rd permu] == True
          # else: do nothing
          if doubleDict[r[-3:-1]] == True: #undo invert for red LSB
              r = r[:-1] + ('1' if r[-1:] == '0' else '0')
          if doubleDict[g[-3:-1]] == True: #undo invert for green LSB
              g = g[:-1] + ('1' if g[-1:] == '0' else '0')
          if doubleDict[b[-3:-1]] == True: #undo invert for blue LSB
              b = b[:-1] + ('1' if b[-1:] == '0' else '0')

          print(f'RED: {r}')
          print(f'GREEN: {g}')
          print(f'BLUE: {b}')

          binary_data += r[-1] #extracting data from the least significant bit of red pixel
          binary_data += g[-1] #extracting data from the least significant bit of red pixel
          binary_data += b[-1] #extracting data from the least significant bit of red pixel

  # split by 8-bits
  all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
  print(f'All bytes {all_bytes}')
  # convert from bits to characters
  decoded_data = ""
  for byte in all_bytes:
      decoded_data += chr(int(byte, 2))
      if decoded_data[-5:-4] == "#": #check if we have reached the delimeter which is "#"
          break
  #print(decoded_data)
  #hash_index = decoded_data.index('#')
  return decoded_data #remove the delimeter to show the original hidden message


# Encode data into image 
def encode_text(): 
  image_name = input("Enter image name(with extension): ") 
  image = cv2.imread(image_name) # Read the input image using OpenCV-Python.
  #It is a library of Python bindings designed to solve computer vision problems. 
  
  #details of the image
  print("The shape of the image is: ",image.shape) #check the shape of image to calculate the number of bytes in it
  print("The original image is as shown below: ")
  resized_image = cv2.resize(image, (500, 500)) #resize the image as per your requirement
  #cv2_imshow(resized_image) #display the image
  
      
  data = input("Enter data to be encoded : ")
  print('Type of data', type(data))
  if (len(data) == 0): 
    raise ValueError('Data is empty')
  
  filename = input("Enter the name of new encoded image(with extension): ")
  encoded_image = hideData(image, data) # call the hideData function to hide the secret message into the selected image
  cv2.imwrite(filename, encoded_image)



# Decode the data in the image 
def decode_text():
  # read the image that contains the hidden image
  image_name = input("Enter the name of the steganographed image that you want to decode (with extension) :") 
  image = cv2.imread(image_name) #read the image using cv2.imread() 

  print("The Steganographed image is as shown below: ")
  resized_image = cv2.resize(image, (500, 500))  #resize the original image as per your requirement
  #cv2_imshow(resized_image) #display the Steganographed image

  # Grab the extract key to undo the invert among the LSBs
  extract_key = input("Enter the extract key of this image (a 4-digit binary string) : ")

  text = showData(image, extract_key)
  return text



# Image Steganography         
def Steganography(): 
    a = input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n Your input is: ")
    userinput = int(a)
    if (userinput == 1):
      print("\nEncoding....")
      encode_text() 
          
    elif (userinput == 2):
      print("\nDecoding....") 
      print("Decoded message is " + decode_text()) 
    else: 
        raise Exception("Enter correct input") 
          
Steganography() #encode image


# In[ ]:


Steganography() #decode image


# In[ ]:




