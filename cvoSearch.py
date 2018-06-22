#title           :cvoSearch.py
#description     :This script is used to look up outbound aliases from "PEEK" file
#instructions    :Must pass "##CVA##," as argument for pattern match in script call
#                :From powershell;; python cvoSearch.py "##CVA##,"
#author          :Jared Noble
#=================================================================================

import re
import sys
import os 
import string
 
_INPUT_FILE = 'peek.txt'
#_INPUT_FILE = 'C:\Users\JN050613\Desktop\peek.txt'
_OUTPUT_FILE = 'peekoutput.txt'
#_OUTPUT_FILE = "C:\\Users\Jared\Desktop\peekoutput1.txt"
 
def main():

#regex search pattern and match parms
  pattern = re.compile('^(.*)' + re.escape(sys.argv[1]) + '(.*)$')
  o = open(_OUTPUT_FILE, 'w')
  with open(_INPUT_FILE) as f:
    for line in f:
      match = pattern.match(line)
      if match is not None:
      #suppress group 1 if you want code values only/2 for nothing useful
        o.write(match.group(1) + match.group(2) + os.linesep)
  o.close()


if __name__ == '__main__':
  main()

#################################################
#Alter output file to append list of code values#
#################################################
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
            # if a comma is identified and tmpStr has a 
            # value then append it to the numbers list
        #elif char == ',' and tmpStr != '':
            #numbers.append(int(tmpStr))
            #tmpStr = ''
    # if tmpStr contains a number add it to the numbers list
    if tmpStr.isdigit():
        numbers.append(int(tmpStr))
# Output the number list
#Insert select statement
tempFile.write("select * from code_value_outbound where code_value in (")
for item in numbers:
  tempFile.write("%s\n" % item + ",")
#Constraints for the query
contrib = input("What is the contributor source? ")
aliasVal = input("Alias value(enter for DONOTSEND): ")
if aliasVal == "":
	tempFile.write(")\nand alias = 'DONOTSEND'\nand contributor_source_cd = " + contrib )
elif aliasVal != "DONOTSEND":
	userInput = aliasVal
	tempFile.write(")\nand alias = '" + userInput + "'\nand contributor_source_cd = " + contrib )
else:
	tempFile.write(")\nand alias = 'DONOTSEND'\nand contributor_source_cd = " + contrib )

tempFile.close()
