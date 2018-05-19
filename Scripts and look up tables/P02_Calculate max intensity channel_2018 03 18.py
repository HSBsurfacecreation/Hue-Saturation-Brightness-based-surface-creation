# Script was tested using WinPython 3.5.1.3.
# Script written by Jackson Li LiangYao. email: li0002on@e.ntu.edu.sg
# Last modified: 2018 03 18 (YYYY MM DD)

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
parser.add_argument("-c", "--chNumbers", type=str, dest="chNumbers", default=["00", "01", "02", "03"], nargs="+", help="chNumbers")
parser.add_argument("-m", "--minValues", type=int, dest="minValues", default=[4, 0, 31, 736], nargs="+", help="minValues")
parser.add_argument("-x", "--maxValues", type=int, dest="maxValues", default=[4079, 4079, 4079, 1155], nargs="+", help="maxValues")
parser.add_argument("-o", "--outScaleFactor", type=float, dest="outScaleFactor", default=10000.0, help="outScaleFactor")
parser.add_argument("-u", "--outChNumber", type=str, dest="outChNumber", default="10", help="outChNumber")
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



# Choose directory to analyse

#tkinter.Tk().withdraw()
#tkinter.messagebox.showinfo("Instructions","Choose folder where images to merge are kept. <Folder P01>")

#dirOfFilesToAnalyze = tkinter.filedialog.askdirectory()
os.chdir(dirOfFilesToAnalyze)
print("Directory chosen: " + dirOfFilesToAnalyze)

print("...Started processing. Please wait until program says it is done.")



# Create Subdirectory

newDirectoryName = "P02_Calculated Max Intensity Channel"
makeSubfolder(newDirectoryName)



# Create Log File

logFileName = "P02 Calculated Max Intensity Channel_log.txt"
logFile = open(newDirectoryName + '/' + logFileName, 'w')
logFile.write("minValues = " + str(repr(minValues)) + '\n')
logFile.write("maxValues = " + str(repr(maxValues)) + '\n')
logFile.write("chNumbers = " + str(repr(chNumbers)) + '\n')
logFile.write("outScaleFactor = " + str(repr(outScaleFactor)) + '\n')
logFile.write("outChNumber = " + str(repr(outChNumber)) + '\n')

logFile.write("\ndirOfFilesToAnalyze: " + str(dirOfFilesToAnalyze) + '\n')
logFile.write("newDirectoryName: " + str(newDirectoryName) + '\n\n')


try:

	# Read in list of p, t, c, x, y, z values of files in same folder.

	dirList = os.listdir(dirOfFilesToAnalyze)
	pList = []
	tList = []
	cList = []
	xList = []
	yList = []
	zList = []

	for name in dirList:
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



	#Analyse files

	for pV in pListCleaned:
		for tV in tListCleaned:
			for xV in xListCleaned:
				for yV in yListCleaned:
					for zV in zListCleaned:

						#Choose image filenames to work on

						qcArray = []

						for cV in chNumbers:
							filename = pV + "_t" + str(tV) + "_c" + str(cV).zfill(2) + "_x" + str(xV) + "_y" + str(yV) + "_z" + str(zV) + ".tif"
							img = openAsArray(filename)
							qcArray.append(img)

						#Perform linear scaling
						qcArray = numpy.array(qcArray)

						for j, cV in enumerate(chNumbers):
							qcArray[j] = ( (qcArray[j] - minValues[j])/(maxValues[j] - minValues[j]) * 1.0).clip(min=0, max=1)

						chOut = numpy.max(qcArray, axis=0) * outScaleFactor


						# Saving the output

						filenameOut = str(pV)+"_t"+str(tV)+"_c"+str(outChNumber).zfill(2)+"_x"+str(xV)+"_y"+str(yV)+"_z"+str(zV)+".tif"
						saveAsImage(chOut, './' + newDirectoryName + '/' + filenameOut)
						print(filenameOut + " was saved...")
						logFile.write(filenameOut + " was saved..." + '\n')



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