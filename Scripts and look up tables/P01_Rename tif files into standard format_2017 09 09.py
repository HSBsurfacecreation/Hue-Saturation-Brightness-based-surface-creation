# Script was tested using WinPython 3.5.1.3.
# Script written by Jackson Li LiangYao. email: li0002on@e.ntu.edu.sg
# Last modified: 2017 09 09 (YYYY MM DD)

# Define parameters here.

# See help at https://docs.python.org/3/library/re.html
# Or read tutorials for "python re.match" on internet

# Example: 't0001_c02_xy_z0003.registered.tif'  --->  '(t) (0000) (_c) (00) (_xy) (_z) (0000) (.registered) (.tif)'
matchString = '(t)(\d*)(_c)(\d*)(_xy)(_z)(\d*)(\.registered)(\.tif)'

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
parser = argparse.ArgumentParser(description='Rename TIF files to standard format')
parser.add_argument("-n", "--nogui", dest="nogui", action="store_true", help="No GUI, use command line")
parser.add_argument("-d", "--dirOfFilesToAnalyze", type=str, dest="dirOfFilesToAnalyze", default=".", help="dirOfFilesToAnalyze")
parser.add_argument("-m", "--match", type=str, dest="matchString", default="(t)(\d*)(_c)(\d*)(_xy)(_z)(\d*)(\.registered)(\.tif)", help="Match string")
parser.add_argument("-p", "--prefix", type=str, dest="prefix", default="q", help="Prefix")
parser.add_argument("-t", "--ttt", type=int, dest="ttt", default="2", help="ttt")
parser.add_argument("-c", "--ccc", type=int, dest="ccc", default="4", help="ccc")
parser.add_argument("-x", "--xxx", type=int, dest="xxx", default="-1", help="xxx")
parser.add_argument("-y", "--yyy", type=int, dest="yyy", default="-1", help="yyy")
parser.add_argument("-z", "--zzz", type=int, dest="zzz", default="7", help="zzz")
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



# Choose directory to analyse

#tkinter.Tk().withdraw()
#tkinter.messagebox.showinfo("Instructions", "Please choose the folder where the tif files are present.")

#dirOfFilesToAnalyze = tkinter.filedialog.askdirectory()
os.chdir(dirOfFilesToAnalyze)
print("Directory chosen: "+dirOfFilesToAnalyze)

print("...Started processing. Please wait until program says it is done.")



# Create Subdirectory

newDirectoryName = "P01_Renamed TIFs"
makeSubfolder(newDirectoryName)



# Create Log File

logFileName = "P01_Rename TIF files_log.txt"
logFile = open(newDirectoryName + '/' + logFileName, 'w')
logFile.write("matchString = " + "'" + str(matchString) + "'" + '\n')
logFile.write("ttt = " + str(repr(ttt)) + '\n')
logFile.write("ccc = " + str(repr(ccc)) + '\n')
logFile.write("xxx = " + str(repr(xxx)) + '\n')
logFile.write("yyy = " + str(repr(yyy)) + '\n')
logFile.write("zzz = " + str(repr(zzz)) + '\n')
logFile.write("prefix = " + str(repr(prefix)) + '\n')
logFile.write('\n' + "dirOfFilesToAnalyze: " + str(dirOfFilesToAnalyze) + '\n')


try:
	# Duplicate files first

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



	# Rename files using pattern matching

	for previousFilename in fileList:
		# Custom, as defined by matchString
		if re.match(matchString, previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: Custom" + '\n')
			m = re.match(matchString, previousFilename)

			if (ttt > 0):
				tt = str(int(m.group(ttt)))
			elif (ttt == -1):
				tt = "0"
			else:
				go = 0
				raise Exception("Error: matchString received unknown input for variable 'ttt'! Only integers above 0 or -1 are allowed!")

			if (ccc > 0):
				cc = str(int(m.group(ccc)))
			elif (ccc == -1):
				cc = "0"
			else:
				go = 0
				raise Exception("Error: matchString received unknown input for variable 'ccc'! Only integers above 0 or -1 are allowed!")

			if (xxx > 0):
				xx = str(int(m.group(xxx)))
			elif (xxx == -1):
				xx = "0"
			else:
				go = 0
				raise Exception("Error: matchString received unknown input for variable 'xxx'! Only integers above 0 or -1 are allowed!")

			if (yyy > 0):
				yy = str(int(m.group(yyy)))
			elif (yyy == -1):
				yy = "0"
			else:
				go = 0
				raise Exception("Error: matchString received unknown input for variable 'yyy'! Only integers above 0 or -1 are allowed!")

			if (zzz > 0):
				zz = str(int(m.group(zzz)))
			elif (zzz == -1):
				zz = "0"
			else:
				go = 0
				raise Exception("Error: matchString received unknown input for variable 'zzz'! Only integers above 0, or exactly -1, are allowed!")

			ss = "0"
			ff = "0"
			go = 1

		# FIJI ImageJ
		#tzc #FIJI_t006_z007_c008.tif
		elif re.match('(.*)(_t)(\d*)(_z)(\d*)(_c)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: FIJI tzc" + '\n')
			m = re.match('(.*)(_t)(\d*)(_z)(\d*)(_c)(\d*)(\.tif)', previousFilename)
			tt = str(int(m.group(3)))
			ss = "0"
			cc = str(int(m.group(7)))
			xx = "0"
			yy = "0"
			ff = "0"
			zz = str(int(m.group(5)))
			go = 1

		#tz #FIJI_t009_z010.tif
		elif re.match('(.*)(_t)(\d*)(_z)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: FIJI tz" + '\n')
			m = re.match('(.*)(_t)(\d*)(_z)(\d*)(\.tif)', previousFilename)
			tt = str(int(m.group(3)))
			ss = "0"
			cc = "0"
			xx = "0"
			yy = "0"
			ff = "0"
			zz = str(int(m.group(5)))
			go = 1

		#zc #FIJI_z011_c012.tif
		elif re.match('(.*)(_z)(\d*)(_c)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: FIJI zc" + '\n')
			m = re.match('(.*)(_z)(\d*)(_c)(\d*)(\.tif)', previousFilename)
			tt = "0"
			ss = "0"
			cc = str(int(m.group(5)))
			xx = "0"
			yy = "0"
			ff = "0"
			zz = str(int(m.group(3)))
			go = 1

		#tc #FIJI_t013_c014.tif
		elif re.match('(.*)(_t)(\d*)(_c)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: FIJI tc" + '\n')
			m = re.match('(.*)(_t)(\d*)(_c)(\d*)(\.tif)', previousFilename)
			tt = str(int(m.group(3)))
			ss = "0"
			cc = str(int(m.group(5)))
			xx = "0"
			yy = "0"
			ff = "0"
			zz = "0"
			go = 1

		#c #FIJI_c015.tif
		elif re.match('(.*)(_c)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: FIJI c" + '\n')
			m = re.match('(.*)(_c)(\d*)(\.tif)', previousFilename)
			tt = "0"
			ss = "0"
			cc = str(int(m.group(3)))
			xx = "0"
			yy = "0"
			ff = "0"
			zz = "0"
			go = 1

		#t #FIJI_t016.tif (manual rename using "FIJI_t" as prefix when saving)
		elif re.match('(.*)(_t)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: FIJI t" + '\n')
			m = re.match('(.*)(_t)(\d*)(\.tif)', previousFilename)
			tt = str(int(m.group(3)))
			ss = "0"
			cc = "0"
			xx = "0"
			yy = "0"
			ff = "0"
			zz = "0"
			go = 1

		#TCZ #Imaris_T17_C18_Z019.tif
		elif re.match('(.*)(_T)(\d*)(_C)(\d*)(_Z)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: Imaris TCZ" + '\n')
			m = re.match('(.*)(_T)(\d*)(_C)(\d*)(_Z)(\d*)(\.tif)', previousFilename)
			tt = str(int(m.group(3)))
			ss = "0"
			cc = str(int(m.group(5)))
			xx = "0"
			yy = "0"
			ff = "0"
			zz = str(int(m.group(7)))
			go = 1

		#TZ or T only #Imaris_T20_Z021.tif
		elif re.match('(.*)(_T)(\d*)(_Z)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: Imaris TZ" + '\n')
			m = re.match('(.*)(_T)(\d*)(_Z)(\d*)(\.tif)', previousFilename)
			tt = str(int(m.group(3)))
			ss = "0"
			cc = "0"
			xx = "0"
			yy = "0"
			ff = "0"
			zz = str(int(m.group(5)))
			go = 1

		#CZ or C only #Imaris_C22_Z023.tif
		elif re.match('(.*)(_C)(\d*)(_Z)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: Imaris CZ" + '\n')
			m = re.match('(.*)(_C)(\d*)(_Z)(\d*)(\.tif)', previousFilename)
			tt = "0"
			ss = "0"
			cc = str(int(m.group(3)))
			xx = "0"
			yy = "0"
			ff = "0"
			zz = str(int(m.group(5)))
			go = 1

		#Z #Imaris_Z024.tif
		elif re.match('(.*)(_Z)(\d*)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: Imaris Z" + '\n')
			m = re.match('(.*)(_Z)(\d*)(\.tif)', previousFilename)
			tt = "0"
			ss = "0"
			cc = "0"
			xx = "0"
			yy = "0"
			ff = "0"
			zz = str(int(m.group(3)))
			go = 1

		#z #FIJI0025.tif
		elif re.match('(.*?)(\d+)(\.tif)', previousFilename):
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: FIJI z" + '\n')
			m = re.match('(.*?)(\d+)(\.tif)', previousFilename)
			tt = "0"
			ss = "0"
			cc = "0"
			xx = "0"
			yy = "0"
			ff = "0"
			zz = str(int(m.group(2)))
			go = 1

		else:
			print(previousFilename + " could not be matched!")
			logFile.write("\'" + str(previousFilename) + "\'" + ", Matching mode used: Ignored" + '\n')
			go = 0
		
		if go == 1:
			newFilename = str(prefix) + "_t" + tt.zfill(4) + "_c" + cc.zfill(2) + "_x" + xx.zfill(3) + "_y" + yy.zfill(3) + "_z" + zz.zfill(4) + ".tif"
			os.rename(previousFilename, newFilename)
			print("Renamed \'" + previousFilename + "\'")




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