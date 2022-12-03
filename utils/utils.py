import json, os

def createJSON(path_file): 
	open(path_file, "w").write("{}")

def readJSON(path_file):
	with open(path_file, "r", encoding="utf-8") as jFile:
		data = json.load(jFile)
	jFile.close()
	return data

def checkifexits(path_file):
	return os.path.exists(path_file)

def writeJSON(path_file, data):
	with open(path_file, "w", encoding="utf-8") as jFile:
		json.dump(data, jFile, indent="\t")
	jFile.close()