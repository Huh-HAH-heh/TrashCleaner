
import argparse
import os
from pathlib import Path
def main():

	parser = argparse.ArgumentParser(description="appDorCmd")
	parser.add_argument("path",nargs="?",default=None,help="roadToZDir")
	args = parser.parse_args()
	if args.path:
		targetDir = Path(args.path).resolve()
	else:
		targetDir = Path(os.getcwd()).resolve()
	print(f"roadToZDir={targetDir}")
	if targetDir.exists() and targetDir.is_dir():
		print("zbs")
		allFiles =[item for item in targetDir.rglob("*") if item.is_file()]
		print(f"FilesCount={len(allFiles)}")
		MCount = 0
		for file in allFiles:
			ext = file.suffix.replace(".","").upper()
			if not ext:
				ext = "NullExt"
			newDir = targetDir / ext
			if file.parent == newDir:
				continue
			newDir.mkdir(parents=True,exist_ok=True)
			newPath = newDir / file.name
			try:
				file.rename(newPath )
				print(f"rename: {file.name} ==> {ext}/")
				MCount+=1
			except Exception as e:
				print(f"ERR {file.name}: {e}")
	else :
		print("err")

if __name__=="__main__":
	main()