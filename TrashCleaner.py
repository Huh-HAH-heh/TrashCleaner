
import argparse
import os
from pathlib import Path
def main():

	parser = argparse.ArgumentParser(description="appDorCmd")

	parser.add_argument("path",nargs="?",default=None,help="roadToZDir")
	
	parser.add_argument("-r","--recursive",action="store_true",help="рекОбход подпапок"
	

	args = parser.parse_args()

	if args.path:
		targetDir = Path(args.path).resolve()
	else:
		targetDir = Path(os.getcwd()).resolve()
	print(f"roadToZDir={targetDir}")
	print(f"Recursive mode: {args.recursive}")

	if targetDir.exists() and targetDir.is_dir():
		print("zbs")
		if args.recursive:
			allFiles =[item for item in targetDir.rglob("*") if item.is_file() and item.parent.name != item.suffix.replace(".", "").upper()
]
		else:
			allFiles =[item for item in targetDir.glob("*") if item.is_file() and item.parent.name != item.suffix.replace(".", "").upper()
]
			

		
		print(f"FilesCount={len(allFiles)}")
		MCount = 0

		for file in allFiles:
			ext = file.suffix.replace(".","").upper()
			if not ext:
				ext = "NullExt"
			newDir = targetDir / ext
			if ext in file.parts:
				continue
			

			newDir.mkdir(parents=True,exist_ok=True)
			newPath = newDir / file.name
			if newPath.exists():
				try:
					if file.stat().st_size == newPath.stat().st_size
					print(f"СКИП (размеры совпадают): {file.name}")
                        continue
					except Exception as e:
						print(f"ERR проверки размера {file.name}: {e}")
						continue
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