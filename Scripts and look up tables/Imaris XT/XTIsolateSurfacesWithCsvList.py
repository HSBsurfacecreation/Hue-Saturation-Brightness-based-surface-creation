#
#
#  Isolate Surfaces With Csv List XTension  
#
#  Updated 2016 05 30 by Jackson, NLG lab, SIGN, Singapore
#
#    <CustomTools>
#      <Menu>
#       <Item name="XTIsolateSurfacesWithCsvList" icon="Python" tooltip="Subset out surfaces from csv file with list of matching object IDs">
#         <Command>PythonXT::XTScript(%i)</Command>
#       </Item>
#      </Menu>
#    </CustomTools>

import sys
import ImarisLib
import time
import random
import numpy
import os, tkFileDialog, tkMessageBox
import Tkinter


def XTScript(aImarisId):
	try:
		# Create an ImarisLib object
		vImarisLib = ImarisLib.ImarisLib()

		# Get an imaris object with id aImarisId
		vImaris = vImarisLib.GetApplication(aImarisId)

		# Check if the object is valid
		if vImaris is None:
			print 'Could not connect to Imaris!'
			# Sleep 2 seconds to give the user a chance to see the printed message
			time.sleep(2)
			return

		# Get the factory
		vFactory = vImaris.GetFactory()

		# Get the surpass scene
		vSurpassScene = vImaris.GetSurpassScene()

		# This XTension requires a loaded dataset
		if vSurpassScene is None:
			print 'Please create some Surfaces in the Surpass scene!'
			time.sleep(2)
			return

		# get the surfaces
		vSurfaces = vFactory.ToSurfaces(vImaris.GetSurpassSelection())

		# search the surfaces if not previously selected
		if not vFactory.IsSurfaces(vSurfaces):
			for vChildIndex in range(vSurpassScene.GetNumberOfChildren()):
				vDataItem = vSurpassScene.GetChild(vChildIndex)
				if vSurfaces is None:
					if vFactory.IsSurfaces(vDataItem):
						vSurfaces = vFactory.ToSurfaces(vDataItem)
			# did we find the surfaces?
			if vSurfaces is None:
				print 'Please create some Surfaces in the Surpass scene!'
				time.sleep(2)
				return

		vNumberOfSurfaces = vSurfaces.GetNumberOfSurfaces()
		vSurfacesName = vSurfaces.GetName()
		vSurfaces.SetVisible(0)

		vIds = vSurfaces.GetIds()
		vIdsNp = numpy.array(vIds)

		root = Tkinter.Tk()
		root.withdraw()

		tkMessageBox.showinfo("Instructions", "Please choose csv file with indices in first column. Csv file expects the first row to be headers...")
		fileToRead = tkFileDialog.askopenfilename()

		vCSVInfo = numpy.genfromtxt(fileToRead, delimiter =",", skip_header=1)
		try:
			vInputIds = vCSVInfo[:,0].astype('uint32')
		except:
			vInputIds = vCSVInfo.astype('uint32')
		print(vInputIds)

		vIdsPicked = numpy.searchsorted(vIdsNp, vInputIds)
		print(vIdsPicked)

		# create new group
		vSurfacesGroup = vFactory.CreateDataContainer()
		vSurfacesGroup.SetName(vSurfacesName + '_subset')

		vNewSurfaces = vFactory.CreateSurfaces()
		vNewSurfaces.SetName(vSurfacesName+'_Select')
		vSurfacesGroup.AddChild(vNewSurfaces, -1);

		for vSurfaceIndex in vIdsPicked:
			vNewSurfaces.AddSurface(vSurfaces.GetVertices(vSurfaceIndex), vSurfaces.GetTriangles(vSurfaceIndex), vSurfaces.GetNormals(vSurfaceIndex), vSurfaces.GetTimeIndex(vSurfaceIndex))

		vSurpassScene.AddChild(vSurfacesGroup, -1)

	except:
		print("Error!")
		print("Error: "+str(sys.exc_info()))
		input()
	


