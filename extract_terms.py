import codecs
import collections
import datetime
import os
import re
import sys
import datetime

import bioc
import strings

def process_file(input_filename, concept_ID, converter, term_counter):
	reader = bioc.BioCXMLDocumentReader(input_filename)
	for document in reader:
		for passage in document.passages:
			for annotation in passage.annotations:
				identifier = annotation.infons.get("identifier") or annotation.infons.get("Identifier")
				if identifier != concept_ID:
					continue
				converted_text = converter(annotation.text)
				term_counter[converted_text][annotation.text] += 1
				#print("Adding " + week_text + " = " + annotation.text)

def noop_converter(s):
	return s

def convert_string(token_text):
	# Map to ASCII, lower case
	converted = strings.map_to_ASCII(token_text).lower()
	# Change non-alphanumeric characters to spaces
	converted = re.sub("[^a-z0-9,]", " ", converted)
	# Change multiple spaces into a single space
	converted = converted.strip()
	converted = re.sub("\\s+", " ", converted)
	# Remove spaces between sequences besides digit digit
	converted = re.sub("([^0-9]) ", "\\1", converted)
	converted = re.sub(" ([^0-9])", "\\1", converted)
	#print("Name \"" + name + "\" was processed to \"" + template + "\"")
	return converted

def process(input_path, concept_ID, converter, output_path):
	term_counter = collections.defaultdict(collections.Counter)
	start = datetime.datetime.now()
	if os.path.isdir(input_path):
		print("Processing directory " + input_path)
		# Process any xml files found
		dir = os.listdir(input_path)
		for item in dir:
			input_filename = input_path + "/" + item
			if os.path.isfile(input_filename) and input_filename.endswith(".xml"):
				print("Processing file " + input_filename)
				process_file(input_filename, concept_ID, converter, term_counter)
	elif os.path.isfile(input_path):
		print("Processing file " + input_path)
		# Process directly
		process_file(input_path, concept_ID, converter, term_counter)
	else:  
		raise RuntimeError("Path is not a directory or normal file: " + input_path)
	print("Total processing time = " + str(datetime.datetime.now() - start))
	
	terms = list()
	for converted_term, term_counts in term_counter.items():
		count = sum(term_counts.values())
		canonical_term = term_counts.most_common()[0][0]
		terms.append((count, converted_term, canonical_term))
	terms.sort(reverse = True)
		
	file = codecs.open(output_path, 'w', encoding="utf-8")
	# Write data
	for count, converted_term, canonical_term in terms:
		file.write(str(count) + "\t" + converted_term + "\t" + canonical_term + "\n")
	file.close()

if __name__ == "__main__":
	start = datetime.datetime.now()
	if len(sys.argv) != 5:
		print("Usage: <input> <concept> <use processing> <output>")
		exit()
	input_path = sys.argv[1]
	concept_ID = sys.argv[2]
	use_processing = sys.argv[3]
	output_path = sys.argv[4]
	if (use_processing.lower() == "true"):
		converter = convert_string
	else:
		converter = noop_converter
	process(input_path, concept_ID, converter, output_path)
