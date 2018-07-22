#title           :cvoSearch.py
#description     :This script is used to look up outbound aliases from "PEEK" file
#instructions    :Must pass "##CVA##," as argument for pattern match in script call
#                :From powershell--> python cvoSearch.py "##CVA##,"
#author          :Jared Noble
#=================================================================================

import re
import sys
import os 
import string
 
_INPUT_FILE = 'peek.txt' #Reading from directory you are calling this program from
_OUTPUT_FILE = 'peekoutput.txt' #Writing to directory you are calling this program from

#Optional - Uncomment these lines to specify a working path. Must follow format 'C:\\Users\<Your USER ID>\Desktop\peek.txt'
#_INPUT_FILE = input("Specify working path to read from: ")
#_OUTPUT_FILE = input("Specify working path to write to: ")
 
def read():
#regex search pattern and match parms
  pattern = re.compile('^(.*)' + re.escape(sys.argv[1]) + '(.*)$')
  openOut = open(_OUTPUT_FILE, 'w')
  with open(_INPUT_FILE) as readIn:
    for line in readIn:
      match = pattern.match(line)
      if match is not None:
      #suppress group 1 if you want code values only/2 for nothing useful
        openOut.write(match.group(1) + match.group(2) + os.linesep)
  openOut.close()
read()

#################################################
#Alter output file to append list of code values#
#################################################
def write():
  numbers = list()
  tempFile = open( _OUTPUT_FILE, 'r+' )

  for eachLine in tempFile:
  # setup a temporary variable
      tmpStr = ''
      for char in eachLine:
          # validate if char is a number
          if char.isdigit():
              # if truly a number add it to the tmpStr
              tmpStr += char
          #if a comma is identified and tmpStr has a 
          #value then append it to the numbers list
          elif char == ',' and tmpStr != '':
              numbers.append(int(tmpStr))
              tmpStr = ''
      # if tmpStr contains a number add it to the numbers list
      if tmpStr.isdigit():
          numbers.append(int(tmpStr))

  #Output the numbers list
  #Begin query
  tempFile.write("select * from code_value_outbound\nwhere code_value in (")
  for item in numbers:
    tempFile.write("%s\n" % item +",")
  tempFile.write("0") #false value, not harmful
  #Constraints for the query
  contrib = input("What is the contributor source? ")
  aliasVal = input("Alias value(enter for DONOTSEND, 'NULL' for all alias values): ")
  if aliasVal == "":
    tempFile.write(")\nand alias = 'DONOTSEND'\nand contributor_source_cd = " + contrib )
  elif aliasVal == "NULL":
    tempFile.write(")\nand alias !=NULL \nand contributor_source_cd = " + contrib )
  elif aliasVal != "DONOTSEND":
    tempFile.write(")\nand alias = '" + aliasVal + "'\nand contributor_source_cd = " + contrib )
  else:
    tempFile.write(")\nand alias = 'DONOTSEND'\nand contributor_source_cd = " + contrib )

  tempFile.close()
write()
