import sys
from shell import Run

if len(sys.argv) > 1:
	filename = sys.argv[1]
	Run.run_file(filename)
else:
	sys.stdout.write("Nature Shell ver 0.1.10.00\n")
	Run.start()