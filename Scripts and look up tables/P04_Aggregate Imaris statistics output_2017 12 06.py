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
import pandas

# GUI and command line additions
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--nogui", dest="nogui", action="store_true", help="No GUI, use command line")
parser.add_argument("-d", "--dirOfFilesToAnalyze", type=str, dest="dirOfFilesToAnalyze", default=".", help="dirOfFilesToAnalyze")
parser.add_argument("--prefix", type=str, dest="prefix", default="Testdata", help="prefix")
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
#tkinter.messagebox.showinfo("Instructions", "Choose folder of Imaris output csv files.")

#dirOfFilesToAnalyze = tkinter.filedialog.askdirectory()
os.chdir(dirOfFilesToAnalyze)
print("Directory chosen: "+dirOfFilesToAnalyze)

print("...Started processing. Please wait until program says it is done.")



# Create Subdirectory

newDirectoryName = "P04_Aggregated statistics"
makeSubfolder(newDirectoryName)



# Create Log File

logFileName = "P04_Aggregate statistics files_log.txt"
logFile = open(newDirectoryName + '/' + logFileName, 'w')
logFile.write("prefix = " + str(repr(prefix)) + '\n')

logFile.write("\ndirOfFilesToAnalyze: " + str(dirOfFilesToAnalyze) + '\n')
logFile.write("newDirectoryName: " + str(newDirectoryName) + '\n\n')


# Start Actual script

try:
	# Test likelihood that user has forgotten the rule about no underscores
	basename = os.path.basename(dirOfFilesToAnalyze)
	logFile.write("basename: " + str(basename) + '\n')
	basenameCountUnderscores = basename.count('_')
	logFile.write("basenameCountUnderscores: " + str(basenameCountUnderscores) + '\n')

	if basenameCountUnderscores > 1:
		print("Detected that underscores were possibly used in naming csv files!")
		logFile.write("Detected that underscores were possibly used in naming csv files!" + '\n')

		if tkinter.messagebox.askyesno("Expecting only a single underscore in the folder name!", "Are you sure you want to continue? Excess underscores in csv filenames may cause naming problems downstream..."):
			print("User has chosen to continue the program")
			logFile.write("User has chosen to continue the program" + '\n')
		else:
			raise Exception("User has aborted program.")
	else:
		pass

	# Detect file naming prefix
	if re.match('(.*)(_Statistics)', basename):
		m = re.match('(.*)(_Statistics)', basename)
		front = m.group(1)
	elif re.match('(.*?)(_)(.*)', basename):
		m = re.match('(.*)(_Statistics)', basename)
		front = m.group(1)
	else:
		front = basename
	logFile.write("front: " + str(front) + '\n')


	# Read in names of all files in folder
	fileList = os.listdir(dirOfFilesToAnalyze)


	# Create empty dataframe holder
	compiledDataSpot = pandas.DataFrame()
	compiledDataTrack = pandas.DataFrame()


	# Initiate variable to keep track of whether IDs are read in already (since only need to read once)
	initiatedSpot = 0
	initiatedTrack = 0


	# Define column headers that separate useful from useless columns
	idColumnHead = "ID"    #Read once only (spots)
	tIdColumnHead = "ID"    #Read once only (tracks)
	trackIdColumnHead = "TrackID"    #Read once only (associated track of a spot)
	spacerColumnHead = "Unit"    #Columns in front of this column are useful
	spacerTColumnHead = "Unit"    #Columns in front of this column are useful


	# Read in position columns first
	positionSpotFilename = front+"_Position.csv"
	positionTrackFilename = front+"_Track_Position.csv"

	if positionSpotFilename in fileList:
		print("Reading "+positionSpotFilename+ "...")
		logFile.write("Reading "+positionSpotFilename+ "..." + '\n')
		df = pandas.read_csv(positionSpotFilename, header=2)

		#If position file exists, read in relevant IDs using this file
		initiatedSpot = 1
		print("Spot/Surface csv initiated...")
		logFile.write("Spot/Surface csv initiated..." + '\n')
		compiledDataSpot['sID'] = df[idColumnHead]

		if trackIdColumnHead in df.columns:
			compiledDataSpot['tID'] = df[trackIdColumnHead]
			compiledDataSpot['oID'] = compiledDataSpot['tID']- 1000000000

		temp = df.loc[:,:spacerColumnHead]
		temp = temp.drop(spacerColumnHead, 1)

		if len(temp.columns) == 3:
			compiledDataSpot[['PosX','PosY','PosZ']] = temp
		else:
			raise Exception("Unable to read in 3 columns from xxx_Position.csv file ")

		print("S: Read in "+positionSpotFilename+" successfully...")
		logFile.write("S: Read in "+positionSpotFilename+" successfully..." + '\n')

	if positionTrackFilename in fileList:
		print("Reading "+positionTrackFilename+"...")
		logFile.write("Reading "+positionTrackFilename+"..." + '\n')
		df = pandas.read_csv(positionTrackFilename, header=2)

		#If track_position file exists, read in relevant IDs using this file
		initiatedTrack = 1
		print("Track csv initiated...")
		logFile.write("Track csv initiated..." + '\n')
		compiledDataTrack['tID'] = df[tIdColumnHead]
		compiledDataTrack['oID'] = compiledDataTrack['tID'] - 1000000000
		temp = df.loc[:,:spacerTColumnHead]
		temp = temp.drop(spacerTColumnHead, 1)

		if len(temp.columns) == 3:
			compiledDataTrack[['TrPosMeanX','TrPosMeanY','TrPosMeanZ']] = temp
		else:
			raise Exception("Unable to read in 3 columns from xxx_Position.csv file ")

		print("T: Read in "+positionTrackFilename+" successfully...")
		logFile.write("T: Read in "+positionTrackFilename+" successfully..." + '\n')


	# Aggregate csv files
	for filename in fileList:
		print("Reading "+filename +"...")
		logFile.write("Reading "+filename +"..." + '\n')

		if re.match(positionSpotFilename, filename):    #Skip position file, since checked earlier
			pass
		elif re.match(positionTrackFilename, filename):    #Skip track_position file, since checked earlier
			pass
		elif re.match('('+front+')'+'(_)(.*)(.csv$)', filename):    #Check if it is csv file
			m = re.match('('+front+')'+'(_)(.*)(.csv$)', filename)

			#Obtain new column header title from its filename
			middle = m.group(3)

			#Modify headers for channel-specific parameters
			if re.match('(.*)(Ch=)(\d*)', middle):
				j = re.match('(.*)(Ch=)(\d*)', middle)
				headerName = j.group(1) + j.group(2) + j.group(3).zfill(2)
			else:
				headerName = middle
			safeHeaderName = re.sub('[^a-zA-Z0-9_()\n\.]', '_', headerName)
			middle = safeHeaderName


			#Read in the file
			df = pandas.read_csv(filename, header=2)

			#Check if it is a Spots/Surface or Track file, and assign to correct output csv file
			if 'Category' in df.columns:
				if (df['Category'][0] == "Spot") or (df['Category'][0] == "Surface"):
					#Trigger reading of IDs if it is the first Spot/Surface file
					if initiatedSpot == 0:
						initiatedSpot = 1
						print("Spot/Surface csv initiated...")
						logFile.write("Spot/Surface csv initiated..." + '\n')
						compiledDataSpot['sID'] = df[idColumnHead]

						if trackIdColumnHead in df.columns:
							compiledDataSpot['tID'] = df[trackIdColumnHead]
							compiledDataSpot['oID'] = compiledDataSpot['tID']- 1000000000
					else:
						pass

					#Find and append useful columns to dataframe
					temp = df.loc[:,:spacerColumnHead]
					temp = temp.drop(spacerColumnHead, 1)

					#Test if need to append XYZ for column header
					if len(temp.columns) == 1:
						compiledDataSpot[middle] = temp
						print("S: Read in "+filename+" successfully... [Single]")
						logFile.write("S: Read in "+filename+" successfully... [Single]" + '\n')
					elif len(temp.columns) == 3:
						compiledDataSpot[[middle+'X',middle+'Y',middle+'Z']] = temp
						print("S: Read in "+filename+" successfully... [Triple]")
						logFile.write("S: Read in "+filename+" successfully... [Triple]" + '\n')
					else:
						raise Exception("Unexpected number of columns! Only accepts 1 or 3. Stopping script...")

				elif df['Category'][0] == "Track":
					#Trigger reading of IDs if it is the first Track file
					if initiatedTrack == 0:
						initiatedTrack = 1
						print("Track csv initiated...")
						logFile.write("Track csv initiated..." + '\n')
						compiledDataTrack['tID'] = df[tIdColumnHead]
						compiledDataTrack['oID'] = compiledDataTrack['tID'] - 1000000000
					else:
						pass

					#Find and append useful columns to dataframe
					temp = df.loc[:,:spacerColumnHead]
					temp = temp.drop(spacerColumnHead, 1)

					#Test if need to append XYZ for column header
					if len(temp.columns) == 1:
						compiledDataTrack[middle] = temp
						print("T: Read in "+filename+" successfully... [Single]")
						logFile.write("T: Read in "+filename+" successfully... [Single]" + '\n')
					elif len(temp.columns) == 3:
						compiledDataTrack[[middle+'X',middle+'Y',middle+'Z']] = temp
						print("T: Read in "+filename+" successfully... [Triple]")
						logFile.write("T: Read in "+filename+" successfully... [Triple]" + '\n')
					else:
						raise Exception("Unexpected number of columns! Only accepts 1 or 3. Stopping script...")
				else:
					print(filename+" has unexpected Category, thus ignored...")
					logFile.write(filename+" has unexpected Category, thus ignored..." + '\n')	
			else:
				print(filename+" does not have Category, thus not included...")
				logFile.write(filename+" does not have Category, thus not included..." + '\n')
		else:
			print(filename+" was ignored...")
			logFile.write(filename+" was ignored..." + '\n')


	#Ensure values are FlowJo compatible
	compiledDataSpotMod = pandas.DataFrame()
	compiledDataTrackMod = pandas.DataFrame()

	for colN in compiledDataSpot.columns:
		if (colN == 'sID') or (colN == 'tID') or (colN == 'oID'):
			compiledDataSpotMod[colN] = compiledDataSpot[colN]
		elif (compiledDataSpot[colN].min() >= 0) & (compiledDataSpot[colN].max() <= 1):
			compiledDataSpotMod[colN] = compiledDataSpot[colN] * 10000
		elif (compiledDataSpot[colN].min() < 0) & (compiledDataSpot[colN].min() >= -1) & (compiledDataSpot[colN].max() <= 1):
			compiledDataSpotMod[colN] = compiledDataSpot[colN] * 1000 + 10000
		else:
			compiledDataSpotMod[colN] = compiledDataSpot[colN]

	for colN in compiledDataTrack.columns:
		if (colN == 'sID') or (colN == 'tID') or (colN == 'oID'):
			compiledDataTrackMod[colN] = compiledDataTrack[colN]
		elif (compiledDataTrack[colN].min() >= 0) & (compiledDataTrack[colN].max() <= 1):
			compiledDataTrackMod[colN] = compiledDataTrack[colN] * 10000
		elif (compiledDataTrack[colN].min() < 0) & (compiledDataTrack[colN].min() >= -1) & (compiledDataTrack[colN].max() <= 1):
			compiledDataTrackMod[colN] = compiledDataTrack[colN] * 1000 + 10000
		else:
			compiledDataTrackMod[colN] = compiledDataTrack[colN]

	compiledDataSpotMod = compiledDataSpotMod.fillna(0)
	compiledDataTrackMod = compiledDataTrackMod.fillna(0)


	#Save output csv files
	outputFilename = prefix+"_Objects.csv"
	compiledDataSpotMod.to_csv("./"+newDirectoryName+"/"+outputFilename, header=1, index=0)
	print(os.getcwd()+"/"+newDirectoryName+"/"+outputFilename+" was created...")
	logFile.write(os.getcwd()+"/"+newDirectoryName+"/"+outputFilename+" was created..." + '\n')

	outputFilenameTrack = prefix+"_Tracks.csv"
	compiledDataTrackMod.to_csv("./"+newDirectoryName+"/"+outputFilenameTrack, header=1, index=0)
	print(os.getcwd()+"/"+newDirectoryName+"/"+outputFilenameTrack+" was created...")
	logFile.write(os.getcwd()+"/"+newDirectoryName+"/"+outputFilenameTrack+" was created..." + '\n')




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
