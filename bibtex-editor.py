# bibtex-editor.py #################################################################
# This function is intended to provide the ability to clean/tidy up multiple .bib files
# placed in "targetfolder". The function exports the eddited ".bib" files to a secondary 
# folder "outputFolder" with the rules defined in "ApplyToEachEntry" and 
# "ApplyToEachField" applied to the properties of each reference.

# An excellent tutorial on the bibtexparser can be found at: 
# 	https://bibtexparser.readthedocs.io/en/v1.1.0/tutorial.html

# Author: James A. Douthwaite 2020-01-21

import os
import re
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *

# Configurations
targetFolder = "references"
targetExtension = ".bib"
outputFolder = "editted"

currentFolder = os.path.abspath(os.path.dirname(__file__))
targetFolder = os.path.join(currentFolder,targetFolder)
outputFolder = os.path.join(currentFolder,outputFolder)

# ====== Function definitions ======
def CapitaliseFirstLetterOnly(text):
	# This function simply makes all characters lower case whilst raising
	# the first letter only.
	if (not isinstance(text,str)):
		return text
	#try:
	text = text.lower()			# Make all lower case
	frst = text[0]
	for ind in range(0,len(text)):

		if text[ind] == '{' or text[ind] == " ":
			continue
		else:
			frst = text[ind].upper()
			break
	# ====
	pre = text[:ind]
	post = text[ind+1:]
	text = pre + frst + post
	#except:
	#	print ("Unable to convert text: " + text)
	print ("\n\n")
	return text

# ============== Entry related ===============
def ApplyToEachEntry(entry):
	# This method is applied to the complete entry, which allows specfic
	# actions on each field to be defined here
	for field in entry:
		entry[field] = ApplyToEachField(entry[field])
	if "title" in entry:
		entry["title"] = CapitaliseFirstLetterOnly(entry["title"])

	return entry

def ApplyToEachField(field):
	# This method is applied to all fields of the bibtex-file
	# This allows universal corrections to be defined here.

	#field = field.replace("{", "").replace("}", "")		# Remove uncessary brackets
	return field

def OutputToFile(bibtexDataBase,outputFile):
	with open(outputFile, 'w') as bibtexFile:
		bibtexparser.dump(bibtexDataBase, bibtexFile)
	return

print("Running bibtex formatter on directory '" + targetFolder + "'")

for file in os.listdir(targetFolder): 

	# If the file does not have the desire extension
	if file.endswith(targetExtension) == 0:
		continue
	# Define absolute paths to files
	inputFile  = os.path.join(targetFolder,file)
	outputFile = os.path.join(outputFolder,file)

	print("Target bibtex file: '" + inputFile + "'")

	# Parse bibtex file
	with open(inputFile) as bibtexFile:
		bibtexDB = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(bibtexFile)

	# Iterate through entries
	for i in range(1,len(bibtexDB.entries)):
		bibtexDB.entries[i] = ApplyToEachEntry(bibtexDB.entries[i])

		print(bibtexDB.entries[i])

	# Output to file of same name in a given directory
	OutputToFile(bibtexDB,outputFile)
