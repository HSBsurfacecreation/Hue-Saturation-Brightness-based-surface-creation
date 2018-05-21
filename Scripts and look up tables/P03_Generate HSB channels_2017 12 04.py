# Script was tested using WinPython 3.5.1.3.
# Script written by Jackson Li LiangYao. email: li0002on@e.ntu.edu.sg
# Last modified: 2017 12 04 (YYYY MM DD)

#------------------------------------------------------------------------------
# Start of script. Avoid modifying anything below unless User has experience with Python programming.

# Import modules

import sys
import traceback
import numpy
import tkinter, tkinter.messagebox, tkinter.filedialog
import os
import re

numpy.seterr("ignore")

# GUI and command line additions
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nogui", dest="nogui", action="store_true", help="No GUI, use command line")
parser.add_argument("-d", "--dirOfFilesToAnalyze", type=str, dest="dirOfFilesToAnalyze", default=".", help="dirOfFilesToAnalyze")
parser.add_argument("--inChNumberA", type=str, dest="inChNumberA", default="02", help="inChNumberA")
parser.add_argument("--inChNumberB", type=str, dest="inChNumberB", default="01", help="inChNumberB")
parser.add_argument("--inChNumberC", type=str, dest="inChNumberC", default="00", help="inChNumberC")
parser.add_argument("--sfA", type=float, dest="sfA", default=1.0, help="sfA")
parser.add_argument("--sfB", type=float, dest="sfB", default=1.0, help="sfB")
parser.add_argument("--sfC", type=float, dest="sfC", default=1.0, help="sfC")
parser.add_argument("--minA", type=int, dest="minA", default=50, help="minA")
parser.add_argument("--maxA", type=int, dest="maxA", default=3500, help="maxA")
parser.add_argument("--minB", type=int, dest="minB", default=220, help="minB")
parser.add_argument("--maxB", type=int, dest="maxB", default=3000, help="maxB")
parser.add_argument("--minC", type=int, dest="minC", default=150, help="minC")
parser.add_argument("--maxC", type=int, dest="maxC", default=3500, help="maxC")
parser.add_argument("--outChNumberH", type=str, dest="outChNumberH", default="67", help="outChNumberH")
parser.add_argument("--outChNumberS", type=str, dest="outChNumberS", default="66", help="outChNumberS")
parser.add_argument("--outChNumberB", type=str, dest="outChNumberB", default="65", help="outChNumberB")
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



def obtain_mask(r,g,b):
	k = (r>0) | (g>0) | (b>0)
	return k

def RGB_to_hsv(r,g,b,rMin,rMax,gMin,gMax,bMin,bMax,sfR,sfG,sfB,k):
	import numpy
	rr = ( (r - rMin)/(rMax - rMin) * 1.0 * sfR ).clip(min=0, max=1)
	gg = ( (g - gMin)/(gMax - gMin) * 1.0 * sfG ).clip(min=0, max=1)
	bb = ( (b - bMin)/(bMax - bMin) * 1.0 * sfB ).clip(min=0, max=1)
	h = numpy.zeros_like(r).astype("float")
	m = numpy.min([rr,gg,bb], axis=0)
	M = numpy.max([rr,gg,bb], axis=0)
	C = M - m
	j = numpy.argmax([rr,gg,bb], axis=0)
	h[(j==0) & (C!=0)] = numpy.mod( (gg[(j==0) & (C!=0)]-bb[(j==0) & (C!=0)])/C[(j==0) & (C!=0)], 6)
	h[(j==1) & (C!=0)] = (bb[(j==1) & (C!=0)]-rr[(j==1) & (C!=0)])/C[(j==1) & (C!=0)] + 2
	h[(j==2) & (C!=0)] = (rr[(j==2) & (C!=0)]-gg[(j==2) & (C!=0)])/C[(j==2) & (C!=0)] + 4
	h = h + 2
	h[C==0] = 0
	h[k==0] = 0
	h = h*5000
	s = numpy.zeros_like(r).astype("float")
	s[M!=0] = (1 - C[M!=0]/M[M!=0])*10000
	v = numpy.zeros_like(r).astype("float")
	v[k==1] = M[k==1] * 10000
	return h, s, v



# Choose directory to analyse

#tkinter.Tk().withdraw()
#tkinter.messagebox.showinfo("Instructions", "Choose folder where images to calculate Hue, Saturation and Brightness channels are kept. <Folder P02B>")

#dirOfFilesToAnalyze = tkinter.filedialog.askdirectory()
os.chdir(dirOfFilesToAnalyze)
print("Directory chosen: " + dirOfFilesToAnalyze)

print("...Started processing. Please wait until program says it is done.")



# Create Subdirectory

newDirectoryName = "P03_HSB"
makeSubfolder(newDirectoryName)



# Create Log File

logFileName = "P03_Generate HSB channels_log.txt"
logFile = open(newDirectoryName + '/' + logFileName, 'w')
logFile.write("inChNumberA = " + str(repr(inChNumberA)) + '\n')
logFile.write("inChNumberB = " + str(repr(inChNumberB)) + '\n')
logFile.write("inChNumberC = " + str(repr(inChNumberC)) + '\n')
logFile.write('\n')
logFile.write("sfA = " + str(repr(sfA)) + '\n')
logFile.write("sfB = " + str(repr(sfB)) + '\n')
logFile.write("sfC = " + str(repr(sfC)) + '\n')
logFile.write('\n')
logFile.write("minA = " + str(repr(minA)) + '\n')
logFile.write("maxA = " + str(repr(maxA)) + '\n')
logFile.write("minB = " + str(repr(minB)) + '\n')
logFile.write("maxB = " + str(repr(maxB)) + '\n')
logFile.write("minC = " + str(repr(minC)) + '\n')
logFile.write("maxC = " + str(repr(maxC)) + '\n')
logFile.write('\n')
logFile.write("outChNumberH = " + str(repr(outChNumberH)) + '\n')
logFile.write("outChNumberS = " + str(repr(outChNumberS)) + '\n')
logFile.write("outChNumberB = " + str(repr(outChNumberB)) + '\n')

logFile.write("\ndirOfFilesToAnalyze: " + str(dirOfFilesToAnalyze) + '\n')
logFile.write("newDirectoryName: " + str(newDirectoryName) + '\n\n')



try:

	# Read in list of p, t, c, x, y, z values of files in same folder.

	dirList = os.listdir(dirOfFilesToAnalyze)
	pList = []
	tList = []
	#cList = []
	xList = []
	yList = []
	zList = []

	for name in dirList:
		if re.match('(.*)(_t)(\d*)(_c)(\d*)(_x)(\d*)(_y)(\d*)(_z)(\d*)(\.tif)', name):
			#To match filename "q_t0000_c00_x000_y000_z0000.tif"
			i = re.match('(.*)(_t)(\d*)(_c)(\d*)(_x)(\d*)(_y)(\d*)(_z)(\d*)(\.tif)', name)
			pList.append(i.group(1))
			tList.append(i.group(3))
			#cList.append(i.group(5))
			xList.append(i.group(7))
			yList.append(i.group(9))
			zList.append(i.group(11))

		else:
			print("\""+name+"\" was ignored.")

	pListCleaned = list(set(pList))
	tListCleaned = list(set(tList))
	#cListCleaned = list(set(cList))
	xListCleaned = list(set(xList))
	yListCleaned = list(set(yList))
	zListCleaned = list(set(zList))
	pListCleaned.sort()
	tListCleaned.sort()
	#cListCleaned.sort()
	xListCleaned.sort()
	yListCleaned.sort()
	zListCleaned.sort()

	logFile.write("pListCleaned: " + str(pListCleaned) + '\n')
	logFile.write("tListCleaned: " + str(tListCleaned) + '\n')
	#logFile.write("cListCleaned: " + str(cListCleaned) + '\n')
	logFile.write("xListCleaned: " + str(xListCleaned) + '\n')
	logFile.write("yListCleaned: " + str(yListCleaned) + '\n')
	logFile.write("zListCleaned: " + str(zListCleaned) + '\n\n')



	# Analyse data

	for pV in pListCleaned:
		for tV in tListCleaned:
			for xV in xListCleaned:
				for yV in yListCleaned:
					for zV in zListCleaned:

							#Choose image filenames to work on

							filenamePmtA = str(pV) + "_t" + str(tV) + "_c" + str(inChNumberA).zfill(2) + "_x" + str(xV) + "_y" + str(yV) + "_z" + str(zV) + ".tif"
							filenamePmtB = str(pV) + "_t" + str(tV) + "_c" + str(inChNumberB).zfill(2) + "_x" + str(xV) + "_y" + str(yV) + "_z" + str(zV) + ".tif"
							filenamePmtC = str(pV) + "_t" + str(tV) + "_c" + str(inChNumberC).zfill(2) + "_x" + str(xV) + "_y" + str(yV) + "_z" + str(zV) + ".tif"

							print('\n')
							print("Processing " + filenamePmtA + ", " + filenamePmtB + ", " + filenamePmtC + "...")


			
							#Open images and convert to numpy data	

							arA = openAsArray(filenamePmtA)*1.0
							arB = openAsArray(filenamePmtB)*1.0
							arC = openAsArray(filenamePmtC)*1.0

							mask = obtain_mask(arA,arB,arC)
							hue, sat, val = RGB_to_hsv(arA, arB, arC, minA, maxA, minB, maxB, minC, maxC,sfA, sfB, sfC, mask)
							print("RGB to HSB ok")



							# Saving the output

							filenameOut = str(pV) + "_t" + str(tV) + "_c" + str(outChNumberH).zfill(2) + "_x" + str(xV) + "_y" + str(yV) + "_z" + str(zV) + ".tif"
							saveAsImage(hue, './' + newDirectoryName + "/" + filenameOut)
							print(filenameOut + " was saved...")
							logFile.write(filenameOut + " was saved..." + '\n')

							filenameOut = str(pV) + "_t" + str(tV) + "_c" + str(outChNumberS).zfill(2) + "_x" + str(xV) + "_y" + str(yV) + "_z" + str(zV) + ".tif"
							saveAsImage(sat, './' + newDirectoryName + "/" + filenameOut)
							print(filenameOut + " was saved...")
							logFile.write(filenameOut + " was saved..." + '\n')

							filenameOut = str(pV) + "_t" + str(tV) + "_c" + str(outChNumberB).zfill(2) + "_x" + str(xV) + "_y" + str(yV) + "_z" + str(zV) + ".tif"
							saveAsImage(val, './' + newDirectoryName + "/" + filenameOut)
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

