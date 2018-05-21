# Script was tested using WinPython 3.5.1.3.
# Script written by Jackson Li LiangYao. email: li0002on@e.ntu.edu.sg
# Last modified: 2017 12 06 (YYYY MM DD)

#------------------------------------------------------------------------------
# Start of script. Avoid modifying anything below unless User has experience with Python programming.

# Import modules

import sys
import traceback
import numpy
import tkinter, tkinter.messagebox, tkinter.filedialog
import os
import re

# GUI and command line additions
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nogui", dest="nogui", action="store_true", help="No GUI, use command line")
parser.add_argument("-d", "--dirOfFilesToAnalyze", type=str, dest="dirOfFilesToAnalyze", default=".", help="dirOfFilesToAnalyze")
parser.add_argument("--inChNumbers", type=str, dest="inChNumbers", default=['00','01'], nargs="+", help="inChNumbers")
parser.add_argument("--cMatrix", type=str, dest="cMatrix", default="[[1.0, 0.3519], [0.2276, 1.0]]", help="cMatrix")
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

# addition processing of cMatrix
cMatrix = eval(cMatrix)

# Define functions

def makeSubfolder(subfoldername):
	import os
	if not os.path.isdir("./" + subfoldername + "/"):
			os.mkdir("./" + subfoldername + "/")
			print( "New folder called "+ "\'" + subfoldername + "\'" + " created" )


def openAsArray(filename, mode="F", type='float'):
	import PIL.Image, numpy
	im = numpy.array(PIL.Image.open(filename).convert(mode)).astype(type)
	return im


def saveAsImage(array, filename, mode="F"):
	import scipy.misc
	scipy.misc.toimage(array, mode=mode).save(filename)


def generateCompensationMatrixXY(cMatrix, imageShape):
	import numpy
	M0 = cMatrix.T
	M1 = numpy.full(numpy.hstack([imageShape, M0.shape]), M0)
	return M1


def channelUnmix(arrayOfXYImages, compensationMatrixXY):
	import numpy
	C = numpy.dstack(arrayOfXYImages)
	X0 = numpy.linalg.solve(compensationMatrixXY, C)
	X0mins = X0.min(axis=0).min(axis=0)
	#X1 = X0 - X0mins
	X2 = numpy.transpose(X0, [2,0,1])
	return X2, X0mins



# Choose directory to analyse

#tkinter.Tk().withdraw()
#tkinter.messagebox.showinfo("Instructions", "Choose folder of images where channel unmixing is to be applied. Files must be in this format. e.g. 'XXX_c01_XXX.tif'")
#dirOfFilesToAnalyze = tkinter.filedialog.askdirectory()
os.chdir(dirOfFilesToAnalyze)
print( "Directory chosen: "+dirOfFilesToAnalyze )

print( "...Started processing. Please wait until program says it is done." )


# Create Subdirectory

newDirectoryName = "UnmixedTemp"
makeSubfolder(newDirectoryName)


# Create Log File

logFileName = "Channel unmix_log.txt"
logFile = open(newDirectoryName + '/' + logFileName, 'w')
logFile.write('\n')


# Start procedure

try:
	#Preliminary check of whether parameters have been input correctly
	lengthinChNumbers = len(inChNumbers)
	cMatrixNp = numpy.array(cMatrix)
	shapeCMatrix = cMatrixNp.shape
	if shapeCMatrix[0] != shapeCMatrix[0]:
		raise Exception('Compensation matrix must be N x N in shape!')
	if shapeCMatrix[0] != lengthinChNumbers:
		raise Exception('Matrix must be NxN in size, where N is the number of channels!')
	if any(isinstance(x, int) for x in inChNumbers):
		raise Exception('You need to enclose your channel numbers with apostrophes!')


	# Read in names of all files in folder
	fileList = os.listdir(os.getcwd())
	logFile.write("fileList: " + str(fileList) + '\n')

	# Identify all files present in folder
	nList = []

	for name in fileList:
		#To match filename "q_t000_c01_s0_i05_x0_y0_z001.tif"
		if re.match('(.*)(_c)(\d*)(.*)(\.tif)', name):
			k = re.match('(.*)(_c)(\d*)(.*)(\.tif)', name)
			nList.append((k.group(1), k.group(4)))
		else:
			print( "\""+name+"\" was ignored." )
			logFile.write("\""+name+"\" was ignored." + '\n')

	nListSet = list(set(nList))
	nListSet.sort()

	# Read in first image to get size of images
	filename0 = nListSet[0][0]+'_c'+inChNumbers[0]+nListSet[0][1]+'.tif'
	image0 = openAsArray(filename0)
	imageShape = image0.shape
	print(imageShape)
	compensationMatrixXY = generateCompensationMatrixXY(cMatrix=cMatrixNp, imageShape=imageShape)

	# Perform channel unmixing, save as 32 bit with negative numbers possible
	runningMins = numpy.zeros(lengthinChNumbers)
	for name in nListSet:
		imageArrayList = []
		for cV in inChNumbers:
			filename = name[0]+'_c'+cV+name[1]+'.tif'
			print(filename)
			image = openAsArray(filename)
			imageArrayList.append(image)
		imageArray = numpy.array(imageArrayList)
		outputImages, mins = channelUnmix(arrayOfXYImages=imageArray, compensationMatrixXY=compensationMatrixXY)
		runningMins = numpy.min([runningMins, mins], axis=0)
		print(mins, runningMins)
		for j, arr in enumerate(outputImages):
			filename2 = name[0]+'_c'+inChNumbers[j]+name[1]+'.tif'
			saveAsImage(arr, newDirectoryName+'/'+filename2)
	print("Finished calculations. Now proceeding to correct images...\n")

	# Correct images to set to start from zero

	newDirectoryName2 = "S01_Unmixed"
	makeSubfolder(newDirectoryName2)

	for name in nListSet:
		for j, cV in enumerate(inChNumbers):
			filename2 = name[0]+'_c'+cV+name[1]+'.tif'
			print(filename2)
			image = openAsArray(newDirectoryName+'/'+filename2)
			imageOut = image - runningMins[j]
			filename3 = filename2
			saveAsImage(imageOut, newDirectoryName2+'/'+filename3)




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




