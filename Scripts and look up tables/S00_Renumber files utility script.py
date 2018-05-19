# Script was tested using WinPython 3.5.1.3.
# Script written by Jackson Li LiangYao. email: li0002on@e.ntu.edu.sg
# Last modified: 2016 06 06 (YYYY MM DD)

#------------------------------------------------------------------------------
# Start of script. Avoid modifying anything below unless User has experience with Python programming.

# Import modules

import sys
import traceback
import numpy
import tkinter, tkinter.messagebox, tkinter.filedialog
import os
import re
import shutil

# GUI and command line additions
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nogui", dest="nogui", action="store_true", help="No GUI, use command line")
parser.add_argument("-d", "--dirOfFilesToAnalyze", type=str, dest="dirOfFilesToAnalyze", default=".", help="dirOfFilesToAnalyze")
parser.add_argument("--tForceAdjacent", type=int, dest="tForceAdjacent", default=0, help="tForceAdjacent")
parser.add_argument("--tRestartNumbering", type=int, dest="tRestartNumbering", default=1, help="tRestartNumbering")
parser.add_argument("--tFlipSequence", type=int, dest="tFlipSequence", default=0, help="tFlipSequence")
parser.add_argument("--cForceAdjacent", type=int, dest="cForceAdjacent", default=0, help="cForceAdjacent")
parser.add_argument("--cRestartNumbering", type=int, dest="cRestartNumbering", default=1, help="cRestartNumbering")
parser.add_argument("--cFlipSequence", type=int, dest="cFlipSequence", default=0, help="cFlipSequence")
parser.add_argument("--xForceAdjacent", type=int, dest="xForceAdjacent", default=0, help="xForceAdjacent")
parser.add_argument("--xRestartNumbering", type=int, dest="xRestartNumbering", default=1, help="xRestartNumbering")
parser.add_argument("--xFlipSequence", type=int, dest="xFlipSequence", default=0, help="xFlipSequence")
parser.add_argument("--yForceAdjacent", type=int, dest="yForceAdjacent", default=0, help="yForceAdjacent")
parser.add_argument("--yRestartNumbering", type=int, dest="yRestartNumbering", default=1, help="yRestartNumbering")
parser.add_argument("--yFlipSequence", type=int, dest="yFlipSequence", default=0, help="yFlipSequence")
parser.add_argument("--zForceAdjacent", type=int, dest="zForceAdjacent", default=0, help="zForceAdjacent")
parser.add_argument("--zRestartNumbering", type=int, dest="zRestartNumbering", default=1, help="zRestartNumbering")
parser.add_argument("--zFlipSequence", type=int, dest="zFlipSequence", default=0, help="zFlipSequence")
parser.add_argument("--tRestartNumber", type=int, dest="tRestartNumber", default=0, help="tRestartNumber")
parser.add_argument("--cRestartNumber", type=int, dest="cRestartNumber", default=0, help="cRestartNumber")
parser.add_argument("--xRestartNumber", type=int, dest="xRestartNumber", default=0, help="xRestartNumber")
parser.add_argument("--yRestartNumber", type=int, dest="yRestartNumber", default=0, help="yRestartNumber")
parser.add_argument("--zRestartNumber", type=int, dest="zRestartNumber", default=0, help="zRestartNumber")
parser.add_argument("--pOverrideExisting", type=int, dest="pOverrideExisting", default=0, help="pOverrideExisting")
parser.add_argument("--pOverrideString", type=str, dest="pOverrideString", default="q", help="pOverrideString")
parser.add_argument("--swapAxis", type=int, dest="swapAxis", default=0, help="swapAxis")
parser.add_argument("--axesToSwap", type=str, dest="axesToSwap", default="xy", help="axesToSwap")
opts = parser.parse_args()

# create the gui using the parser
class Window(tkinter.Frame):
	import tkinter
	class DirButton(tkinter.Button):
		def __init__(self, bound_variable, **options):
			import tkinter
			self.bound_variable = bound_variable
			tkinter.Button.__init__(self, command=self.selectDirectory, **options)
		def selectDirectory(self):
			self.bound_variable.set(tkinter.filedialog.askdirectory())
	def __init__(self, master, parser):
		import tkinter, argparse
		tkinter.Frame.__init__(self, master)
		self.gui_ok = False
		self.master = master
		self.master.title("")
		self.grid()
		self.values = {}
		self.parser = parser
		self.opts = {}
		row = 0
		for option in parser._actions:
			if isinstance(option, argparse._StoreAction):
				# directory
				if option.dest == "dirOfFilesToAnalyze":
					self.values[option.dest] = tkinter.StringVar()
					self.values[option.dest].set(option.default)
					# directory location
					tkinter.Label(text="Directory : ", anchor="w").grid(row=row, column=0, sticky="W")
					tkinter.Label(textvariable=self.values[option.dest], width=100, anchor="w").grid(row=row, column=1, sticky="W")
					self.DirButton(self.values[option.dest], text="Select directory").grid(row=row, column=2, sticky="W")
				elif option.type == str or option.type == float or option.type == int:
					self.values[option.dest] = tkinter.StringVar()
					if type(option.default) == list or type(option.default) == tuple:
						self.values[option.dest].set(" ".join(map(str, option.default)))
					else:
						self.values[option.dest].set(option.default)
					tkinter.Label(text="%s : " % option.help, anchor="w").grid(row=row, column=0, sticky="W")
					tkinter.Entry(textvariable=self.values[option.dest], width=100).grid(row=row, column=1, columnspan=2, sticky="W")
				else:
					print("Not sure what to do with %s" % option)
					sys.exit(1)
				row += 1
		# add the buttons
		tkinter.Button(text="Done", command=self.done).grid(row=row, column=0, columnspan=1)
		tkinter.Button(text="Cancel", command=lambda: self.master.destroy()).grid(row=row, column=1, columnspan=2, sticky="W")
	def check(self):
		import argparse, sys
		self.opts = {}
		errors = []
		for option in self.parser._actions:
			if isinstance(option, argparse._StoreAction):
				# array input
				if option.nargs == "+":
					if option.type == float:
						try:
							self.opts[option.dest] = list(map(float, self.values[option.dest].get().replace(",", " ").split()))
						except:
							errors.append("Option %s needs a proper floating point number" % option.help)
					elif option.type == int:
						try:
							self.opts[option.dest] = list(map(int, self.values[option.dest].get().replace(",", " ").split()))
						except:
							errors.append("Option %s needs a proper integer" % option.help)
					elif option.type == str:
						try:
							self.opts[option.dest] = list(map(str, self.values[option.dest].get().replace(",", " ").split()))
						except:
							errors.append("Option %s needs a proper string" % option.help)
					else:
						errors.append("Unknown error with %s" % option.help)
				else:					
					if option.type == float:
						try:
							self.opts[option.dest] = float(self.values[option.dest].get())
						except:
							errors.append("Option %s needs a proper floating point number" % option.help)
					elif option.type == int:
						try:
							self.opts[option.dest] = int(self.values[option.dest].get())
						except:
							errors.append("Option %s needs a proper integer" % option.help)
					elif option.type == str:
						try:
							self.opts[option.dest] = str(self.values[option.dest].get())
						except:
							errors.append("Option %s needs a proper string" % option.help)
					else:
						errors.append("Unknown error with %s" % option.help)
		return errors
	def done(self):
		import tkinter
		errors = self.check()
		if len(errors) == 0:
			self.gui_ok = True
			self.master.destroy()
		else:
			tkinter.messagebox.showinfo("Errors detected", "The following errors were found:\n\n%s" % "\n".join(errors))
			
if not opts.nogui:
	root = tkinter.Tk()
	app = Window(root, parser)
	root.mainloop()
	if not app.gui_ok:
		print("User cancelled.")
		sys.exit(1)
	else:
		# set the globals
		for key in app.opts.keys():
			globals()[key] = app.opts[key]
else:
	# set the globals
	for key in vars(opts).keys():
		if key != "nogui":
			globals()[key] = vars(opts)[key]

# Define functions

def makeSubfolder(subfoldername):
	import os
	if not os.path.isdir("./" + subfoldername + "/"):
			os.mkdir("./" + subfoldername + "/")
			print("New folder called "+ "\'" + subfoldername + "\'" + " created")

def openAsArray(filename, mode="F", type='float'):
	import PIL.Image, numpy
	im = numpy.array(PIL.Image.open(filename).convert(mode)).astype(type)
	return im

def saveAsImage(array, filename, mode="F"):
	import scipy.misc
	scipy.misc.toimage(array, mode=mode).save(filename)



def transformSequence(nOld, nForceAdjacent=0, nRestartNumbering=0, nFlipSequence=0, nRestartNumber=0):
	import numpy
	nMin = nOld.min()
	nNew = nOld.copy()
	if nForceAdjacent == 1:
		nNew = numpy.array([(i + nMin) for (i, v) in enumerate(nOld)])
	else:
		pass

	if nRestartNumbering == 1:
		nDiff = nMin - int(nRestartNumber)
		nNew = nNew - nDiff
	else:
		pass

	if nFlipSequence == 1:
		nNew = nNew[::-1]
	else:
		pass

	return nNew



def replaceSequence(nOld, nOverrideExisting=0, nOverrideString="q"):
	import numpy
	nNew = nOld.copy()
	if nOverrideExisting == 1:
		nNew = numpy.array([nOverrideString for v in nOld])
	return nNew


# Choose directory to analyse

#tkinter.Tk().withdraw()
#tkinter.messagebox.showinfo("Instructions", "Choose folder where images to be renumbered are kept. Existing files must already be in standard format: \'q_t0000_c01_x002_y003_z0004.tif\'")

#dirOfFilesToAnalyze = tkinter.filedialog.askdirectory()
os.chdir(dirOfFilesToAnalyze)
print("Directory chosen: "+dirOfFilesToAnalyze)

print("...Started processing. Please wait until program says it is done.")



# Create Subdirectory

newDirectoryName = "S00_Renumbered TIFs"
makeSubfolder(newDirectoryName)



# Create Log File

logFileName = "S00_Renumber files_log.txt"
logFile = open(newDirectoryName + '/' + logFileName, 'w')
logFile.write("tForceAdjacent = " + str(repr(tForceAdjacent)) + '\n')
logFile.write("tRestartNumbering = " + str(repr(tRestartNumbering)) + '\n')
logFile.write("tFlipSequence = " + str(repr(tFlipSequence)) + '\n')
logFile.write('\n')
logFile.write("cForceAdjacent = " + str(repr(cForceAdjacent)) + '\n')
logFile.write("cRestartNumbering = " + str(repr(cRestartNumbering)) + '\n')
logFile.write("cFlipSequence = " + str(repr(cFlipSequence)) + '\n')
logFile.write('\n')
logFile.write("xForceAdjacent = " + str(repr(xForceAdjacent)) + '\n')
logFile.write("xRestartNumbering = " + str(repr(xRestartNumbering)) + '\n')
logFile.write("xFlipSequence = " + str(repr(xFlipSequence)) + '\n')
logFile.write('\n')
logFile.write("yForceAdjacent = " + str(repr(yForceAdjacent)) + '\n')
logFile.write("yRestartNumbering = " + str(repr(yRestartNumbering)) + '\n')
logFile.write("yFlipSequence = " + str(repr(yFlipSequence)) + '\n')
logFile.write('\n')
logFile.write("zForceAdjacent = " + str(repr(zForceAdjacent)) + '\n')
logFile.write("zRestartNumbering = " + str(repr(zRestartNumbering)) + '\n')
logFile.write("zFlipSequence = " + str(repr(zFlipSequence)) + '\n')
logFile.write('\n')
logFile.write("tRestartNumber = " + str(repr(tRestartNumber)) + '\n')
logFile.write("cRestartNumber = " + str(repr(cRestartNumber)) + '\n')
logFile.write("xRestartNumber = " + str(repr(xRestartNumber)) + '\n')
logFile.write("yRestartNumber = " + str(repr(yRestartNumber)) + '\n')
logFile.write("zRestartNumber = " + str(repr(zRestartNumber)) + '\n')
logFile.write('\n')
logFile.write("pOverrideExisting = " + str(repr(pOverrideExisting)) + '\n')
logFile.write("pOverrideString = " + str(repr(pOverrideString)) + '\n')
logFile.write('\n')
logFile.write("swapAxis = " + str(repr(swapAxis)) + '\n')
logFile.write("axesToSwap = " + str(repr(axesToSwap)) + '\n')
logFile.write('\n')

logFile.write("\ndirOfFilesToAnalyze: " + str(dirOfFilesToAnalyze) + '\n')
logFile.write("newDirectoryName: " + str(newDirectoryName) + '\n\n')




try:
	# Perform error checking for parameter inputs first since mistakes can take a long time to discover

	if not(tForceAdjacent in (0, 1)):
		raise Exception("Parameter 'tForceAdjacent' accepts only '1' or '0'!")

	if not(tRestartNumbering in (0, 1)):
		raise Exception("Parameter 'tRestartNumbering' accepts only '1' or '0'!")

	if not(tFlipSequence in (0, 1)):
		raise Exception("Parameter 'tFlipSequence' accepts only '1' or '0'!")

	if not(cForceAdjacent in (0, 1)):
		raise Exception("Parameter 'cForceAdjacent' accepts only '1' or '0'!")

	if not(cRestartNumbering in (0, 1)):
		raise Exception("Parameter 'cRestartNumbering' accepts only '1' or '0'!")

	if not(cFlipSequence in (0, 1)):
		raise Exception("Parameter 'cFlipSequence' accepts only '1' or '0'!")

	if not(xForceAdjacent in (0, 1)):
		raise Exception("Parameter 'xForceAdjacent' accepts only '1' or '0'!")

	if not(xRestartNumbering in (0, 1)):
		raise Exception("Parameter 'xRestartNumbering' accepts only '1' or '0'!")

	if not(xFlipSequence in (0, 1)):
		raise Exception("Parameter 'xFlipSequence' accepts only '1' or '0'!")

	if not(yForceAdjacent in (0, 1)):
		raise Exception("Parameter 'yForceAdjacent' accepts only '1' or '0'!")

	if not(yRestartNumbering in (0, 1)):
		raise Exception("Parameter 'yRestartNumbering' accepts only '1' or '0'!")

	if not(yFlipSequence in (0, 1)):
		raise Exception("Parameter 'yFlipSequence' accepts only '1' or '0'!")

	if not(zForceAdjacent in (0, 1)):
		raise Exception("Parameter 'zForceAdjacent' accepts only '1' or '0'!")

	if not(zRestartNumbering in (0, 1)):
		raise Exception("Parameter 'zRestartNumbering' accepts only '1' or '0'!")

	if not(zFlipSequence in (0, 1)):
		raise Exception("Parameter 'zFlipSequence' accepts only '1' or '0'!")

	if not(pOverrideExisting in (0, 1)):
		raise Exception("Parameter 'pOverrideExisting' accepts only '1' or '0'!")

	if not(swapAxis in (0, 1)):
		raise Exception("Parameter 'swapAxis' accepts only '1' or '0'!")

	try:
		test = int(tRestartNumber)
	except:
		raise Exception("Parameter 'tRestartNumber' accepts only integers!")

	try:
		test = int(cRestartNumber)
	except:
		raise Exception("Parameter 'cRestartNumber' accepts only integers!")

	try:
		test = int(xRestartNumber)
	except:
		raise Exception("Parameter 'xRestartNumber' accepts only integers!")

	try:
		test = int(yRestartNumber)
	except:
		raise Exception("Parameter 'yRestartNumber' accepts only integers!")

	try:
		test = int(zRestartNumber)
	except:
		raise Exception("Parameter 'zRestartNumber' accepts only integers!")

	try:
		test = str(pOverrideString)
	except:
		raise Exception("Parameter 'pOverrideString' expects only strings!")

	if not(axesToSwap in ('tc', 'tx', 'ty', 'tz', 'cx', 'cy', 'cz', 'xy', 'xz', 'yz')):
		raise Exception("Parameter 'axesToSwap' accepts only the following modes: 'tc', 'tx', 'ty', 'tz', 'cx', 'cy', 'cz', 'xy', 'xz' or 'yz'!")




	# Duplicate files

	print("...Started duplicating files. Please wait.")

	for originalFilename in os.listdir(dirOfFilesToAnalyze):
		if os.path.isfile("./" + originalFilename):
			print("Copying \"" + originalFilename + "\"")
			shutil.copy("./" + originalFilename, "./" + newDirectoryName + "/" + originalFilename)
		else:
			print(originalFilename + " is not a file.")



	# Switch working directory to newly created folder 

	newDirectory = "./" + newDirectoryName + "/"
	os.chdir(newDirectory)
	print("Working in new folder: "+os.getcwd())
	logFile.write("Working in new folder: "+os.getcwd()+'\n\n')



	# Read in names of all files in folder

	fileList = os.listdir(os.getcwd())



	# Read in list of p, t, c, x, y, z values of files in same folder.

	pList = []
	tList = []
	cList = []
	xList = []
	yList = []
	zList = []

	for name in fileList:
		if re.match('(.*)(_t)(\d*)(_c)(\d*)(_x)(\d*)(_y)(\d*)(_z)(\d*)(\.tif)', name):
			#To match filename "q_t0000_c00_x000_y000_z0000.tif"
			i = re.match('(.*)(_t)(\d*)(_c)(\d*)(_x)(\d*)(_y)(\d*)(_z)(\d*)(\.tif)', name)
			pList.append(i.group(1))
			tList.append(i.group(3))
			cList.append(i.group(5))
			xList.append(i.group(7))
			yList.append(i.group(9))
			zList.append(i.group(11))

		else:
			print("\""+name+"\" was ignored.")

	pListCleaned = list(set(pList))
	tListCleaned = list(set(tList))
	cListCleaned = list(set(cList))
	xListCleaned = list(set(xList))
	yListCleaned = list(set(yList))
	zListCleaned = list(set(zList))
	pListCleaned.sort()
	tListCleaned.sort()
	cListCleaned.sort()
	xListCleaned.sort()
	yListCleaned.sort()
	zListCleaned.sort()

	logFile.write("pListCleaned: " + str(pListCleaned) + '\n')
	logFile.write("tListCleaned: " + str(tListCleaned) + '\n')
	logFile.write("cListCleaned: " + str(cListCleaned) + '\n')
	logFile.write("xListCleaned: " + str(xListCleaned) + '\n')
	logFile.write("yListCleaned: " + str(yListCleaned) + '\n')
	logFile.write("zListCleaned: " + str(zListCleaned) + '\n\n')


	# Perform transformations

	pOld = numpy.array(pListCleaned).astype(str)
	tOld = numpy.array(tListCleaned).astype(int)
	cOld = numpy.array(cListCleaned).astype(int)
	xOld = numpy.array(xListCleaned).astype(int)
	yOld = numpy.array(yListCleaned).astype(int)
	zOld = numpy.array(zListCleaned).astype(int)

	tNew = transformSequence(nOld=tOld, nForceAdjacent=tForceAdjacent, nRestartNumbering=tRestartNumbering, nFlipSequence=tFlipSequence, nRestartNumber=int(tRestartNumber))
	cNew = transformSequence(nOld=cOld, nForceAdjacent=cForceAdjacent, nRestartNumbering=cRestartNumbering, nFlipSequence=cFlipSequence, nRestartNumber=int(cRestartNumber))
	xNew = transformSequence(nOld=xOld, nForceAdjacent=xForceAdjacent, nRestartNumbering=xRestartNumbering, nFlipSequence=xFlipSequence, nRestartNumber=int(xRestartNumber))
	yNew = transformSequence(nOld=yOld, nForceAdjacent=yForceAdjacent, nRestartNumbering=yRestartNumbering, nFlipSequence=yFlipSequence, nRestartNumber=int(yRestartNumber))
	zNew = transformSequence(nOld=zOld, nForceAdjacent=zForceAdjacent, nRestartNumbering=zRestartNumbering, nFlipSequence=zFlipSequence, nRestartNumber=int(zRestartNumber))

	pNew = replaceSequence(nOld=pOld, nOverrideExisting=pOverrideExisting, nOverrideString=str(pOverrideString))

	logFile.write("pOld:" + str(pOld) + '\n')
	logFile.write("pNew:" + str(pNew) + '\n')
	logFile.write('\n')
	logFile.write("tOld:" + str(tOld) + '\n')
	logFile.write("tNew:" + str(tNew) + '\n')
	logFile.write('\n')
	logFile.write("cOld:" + str(cOld) + '\n')
	logFile.write("cNew:" + str(cNew) + '\n')
	logFile.write('\n')
	logFile.write("xOld:" + str(xOld) + '\n')
	logFile.write("xNew:" + str(xNew) + '\n')
	logFile.write('\n')
	logFile.write("yOld:" + str(yOld) + '\n')
	logFile.write("yNew:" + str(yNew) + '\n')
	logFile.write('\n')
	logFile.write("zOld:" + str(zOld) + '\n')
	logFile.write("zNew:" + str(zNew) + '\n')
	logFile.write('\n\n')

	# Apply transformations and swaps if necessary

	for pI, pV in enumerate(pOld):
		for tI, tV in enumerate(tOld):
			for cI, cV in enumerate(cOld):
				for xI, xV in enumerate(xOld):
					for yI, yV in enumerate(yOld):
						for zI, zV in enumerate(zOld):

							previousFilename = str(pV) + "_t" + str(tV).zfill(4) + "_c" + str(cV).zfill(2) + "_x" + str(xV).zfill(3) + "_y" + str(yV).zfill(3) + "_z" + str(zV).zfill(4) + ".tif"
							newP = pNew[pI]
							newT = tNew[tI]
							newC = cNew[cI]
							newX = xNew[xI]
							newY = yNew[yI]
							newZ = zNew[zI]

							if swapAxis == 0:
								pass

							elif swapAxis == 1:
								if axesToSwap == "tc":
									newC = tNew[tI]
									newT = cNew[cI]

								elif axesToSwap == "tx":
									newX = tNew[tI]
									newT = xNew[xI]

								elif axesToSwap == "ty":
									newY = tNew[tI]
									newT = yNew[yI]

								elif axesToSwap == "tz":
									newZ = tNew[tI]
									newT = zNew[zI]

								elif axesToSwap == "cx":
									newX = cNew[cI]
									newC = xNew[xI]

								elif axesToSwap == "cy":
									newY = cNew[cI]
									newC = yNew[yI]

								elif axesToSwap == "cz":
									newZ = cNew[cI]
									newC = zNew[zI]

								elif axesToSwap == "xy":
									newY = xNew[xI]
									newX = yNew[yI]

								elif axesToSwap == "xz":
									newZ = xNew[xI]
									newX = zNew[zI]

								elif axesToSwap == "yz":
									newZ = yNew[yI]
									newY = zNew[zI]

								else:
									print("axesToSwap parameter not recognized! Input: " + str(repr(axesToSwap)))
									logFile.write("axesToSwap parameter not recognized! Input: " + str(repr(axesToSwap)) + '\n')
									raise Exception()
							else:
								print("swapAxis parameter not recognized! Input: " + str(repr(swapAxis)))
								logFile.write("swapAxis parameter not recognized! Input: " + str(repr(swapAxis)) + '\n')
								raise Exception()

							newFilename = str(newP) + "_t" + str(newT).zfill(4) + "_c" + str(newC).zfill(2) + "_x" + str(newX).zfill(3) + "_y" + str(newY).zfill(3) + "_z" + str(newZ).zfill(4) + ".tif"
							print(str(previousFilename) + ", " + str(newFilename))
							logFile.write(str(previousFilename) + ", " + str(newFilename) +'\n')
							os.rename(previousFilename, newFilename)




# End of script

except:
	err = traceback.format_exc()
	print(err)
	logFile.write("\nError!\n")
	logFile.write(err)
	logFile.close()

logFile.close()
print("\n...Done.")
if not opts.nogui:
	input("Enter to exit.")

