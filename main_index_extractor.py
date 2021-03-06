# -*- coding: utf-8 -*-
"""
/***************************************************************************
 index_extractor
								 A QGIS plugin
 This plug-in extract several Vegetal Index from Sentinel-2 data
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
							  -------------------
		begin                : 2018-03-08
		git sha              : $Format:%H$
		copyright            : (C) 2018 by Javier Balanzategui Sánchez
		email                : javier.balanzategui.sanchez@alumnos.upm.es
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
#from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
#from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QTableWidget,QTableWidgetItem, QFileDialog, QDialogButtonBox, QMessageBox, QLineEdit
# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .main_index_extractor_dialog import index_extractorDialog
import os.path
#Mine

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from qgis.core import *
import qgis.utils
from qgis.utils import iface

#For calculating VI
from .NitrogenIndex import SpectralIndexes, extract_data, mapper, Coordinates, getXYMinMax
import numpy as np
import osr
import time

#downloads and import a package 
def install_and_import(package):
	import importlib
	try:
		importlib.import_module(package)
	except ImportError:
		import pip
		if package is 'PIL':
			pip.main(['install', 'pillow'])
		else:
			pip.main(['install', package])
	finally:
		globals()[package] = importlib.import_module(package)


class index_extractor:
	"""QGIS Plugin Implementation."""

	def __init__(self, iface):
		"""Constructor.

		:param iface: An interface instance that will be passed to this class
			which provides the hook by which you can manipulate the QGIS
			application at run time.
		:type iface: QgsInterface
		"""
		# Save reference to the QGIS interface
		self.iface = iface
		# initialize plugin directory
		self.plugin_dir = os.path.dirname(__file__)
		# initialize locale
		locale = QSettings().value('locale/userLocale')[0:2]
		locale_path = os.path.join(
			self.plugin_dir,
			'i18n',
			'index_extractor_{}.qm'.format(locale))

		if os.path.exists(locale_path):
			self.translator = QTranslator()
			self.translator.load(locale_path)

			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)

		# Create the dialog (after translation) and keep reference
		self.dlg = index_extractorDialog()

		# Declare instance attributes
		self.actions = []
		self.menu = self.tr(u'&Sentinel-2 Index Extractor')
		# TODO: We are going to let the user set this up in a future iteration
		self.toolbar = self.iface.addToolBar(u'index_extractor')
		self.toolbar.setObjectName(u'index_extractor')


		##CLEAR INPUT BOX AND CALL SELECT IPUT FILE ON-CLICK
		self.dlg.lineEdit.clear()
		self.dlg.pushButton.clicked.connect(self.select_input_file)
		self.dlg.pushButton_2.clicked.connect(self.Select_Unselect)
		self.selectPhase = False
		self.createdOptions = False
		self.shapeBox = None
		self.saveCSV = False
		self.CCCImin = None
		self.CCCImax = None

		

	# noinspection PyMethodMayBeStatic
	def tr(self, message):
		"""Get the translation for a string using Qt translation API.

		We implement this ourselves since we do not inherit QObject.

		:param message: String for translation.
		:type message: str, QString

		:returns: Translated version of message.
		:rtype: QString
		"""
		# noinspection PyTypeChecker,PyArgumentList,PyCallByClass
		return QCoreApplication.translate('index_extractor', message)


	def add_action(
		self,
		icon_path,
		text,
		callback,
		enabled_flag=True,
		add_to_menu=True,
		add_to_toolbar=True,
		status_tip=None,
		whats_this=None,
		parent=None):
		"""Add a toolbar icon to the toolbar.

		:param icon_path: Path to the icon for this action. Can be a resource
			path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
		:type icon_path: str

		:param text: Text that should be shown in menu items for this action.
		:type text: str

		:param callback: Function to be called when the action is triggered.
		:type callback: function

		:param enabled_flag: A flag indicating if the action should be enabled
			by default. Defaults to True.
		:type enabled_flag: bool

		:param add_to_menu: Flag indicating whether the action should also
			be added to the menu. Defaults to True.
		:type add_to_menu: bool

		:param add_to_toolbar: Flag indicating whether the action should also
			be added to the toolbar. Defaults to True.
		:type add_to_toolbar: bool

		:param status_tip: Optional text to show in a popup when mouse pointer
			hovers over the action.
		:type status_tip: str

		:param parent: Parent widget for the new action. Defaults None.
		:type parent: QWidget

		:param whats_this: Optional text to show in the status bar when the
			mouse pointer hovers over the action.

		:returns: The action that was created. Note that the action is also
			added to self.actions list.
		:rtype: QAction
		"""

		icon = QIcon(icon_path)
		action = QAction(icon, text, parent)
		action.triggered.connect(callback)
		action.setEnabled(enabled_flag)

		if status_tip is not None:
			action.setStatusTip(status_tip)

		if whats_this is not None:
			action.setWhatsThis(whats_this)

		if add_to_toolbar:
			self.toolbar.addAction(action)

		if add_to_menu:
			self.iface.addPluginToMenu(
				self.menu,
				action)

		self.actions.append(action)

		return action

	def initGui(self):
		"""Create the menu entries and toolbar icons inside the QGIS GUI."""

		icon_path = ':/plugins/main_index_extractor/icon.png'
		self.add_action(
			icon_path,
			text=self.tr(u'Extract VI from Sentinel-2 data'),
			callback=self.run,
			parent=self.iface.mainWindow())


	def unload(self):
		"""Removes the plugin menu item and icon from QGIS GUI."""
		for action in self.actions:
			self.iface.removePluginMenu(
				self.tr(u'&Sentinel-2 Index Extractor'),
				action)
			self.iface.removeToolBarIcon(action)
		# remove the toolbar
		del self.toolbar

	#Once selected input file, show avaible indexes
	def createDialog(self):
		##ADD NEW VI AND THEIR OPTIONS##

		VI = [ ["Color",["10m (B3)", "20m(B3,B6)", "60m (B1,B3,B6)"]],
					["OTCI", ["10m (B4)", "20m (B4,B5,B6)","60m (B5,B6,B6)"]],
					["MCARI",["10m (B3,B4)","20m (B3,B4,B5)","60m (B3,B4,B5)"]],
					["IRECI",["10m (B4)","20m (B4,B5,B6,B7)","60m (B4,B5,B6,B7)"]],
					["CCCI",["20m (B5,B6,B7)", "60m (B5,B6,B7)"]],
					["NDRE",["20m (B5,B6,B7)", "60m (B5,B6,B7)"]],
					["MTCI", ["10m (B4)", "20m (B4,B5,B6)","60m(B4,B5,B6)"]],
					["CI_redEdge",["20m (B5,B7)","60m (B5,B7)"]],
					["CI_greenEdge",["10m (B3)","20m (B3,B7)","60m (B3,B7)"]],
					["EVI",["10m (B2,B3,B4)","20m (B2,B3,B4)", "60m (B2,B3,B4)"]],
					["NRERI",["10m (B4)","20m (B5,B6,B7)", "60m (B5,B6,B7)"]],
					["NDVI705",["20m (B5,B6)", "60m (B5,B6)"]],
					["mNDVI705",["20m (B5,B6)", "60m (B1,B5,B6)"]],
					["NDI45", ["10m (B4)", "20m (B4,B5)","60m (B4,B5)"]],
					["RDVI", ["10m (B4)", "20m (B4,B7)","60m (B4,B7)"]],
					["TCARI", ["10m (B3,B4)", "20m (B3,B4,B5)", "60m (B3,B4,B5)"]],
					["OSAVI", ["10m (B4)", "20m (B4,B7)", "60m (B4,B7)"]],
					["TCARI/OSAVI", ["10m (B3,B4)", "20m (B3,B4,B5,B7)", "60m (B3,B4,B5,B7)"]]
					]

		self.dlg.tableWidget.setRowCount(0)#Delete al rows before insert
		
		for row in range(len(VI)):
			element = VI[row]

			item = QTableWidgetItem(element[0])

			self.dlg.tableWidget.insertRow(row)
			self.dlg.tableWidget.setItem(row,0,item)#VI name
			for options_n in range(len(element[1])):

				opt = QTableWidgetItem(element[1][options_n])
				opt.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
				opt.setCheckState(Qt.Unchecked)

				self.dlg.tableWidget.setItem(row,options_n+1,opt)#VI options

			if element[0] == "CCCI":
				#add input boxes for min max resample
				item = QTableWidgetItem("0.62")
				item2 = QTableWidgetItem("0.24")
				item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled )
				item2.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled)
				item.setToolTip("Max value")
				item2.setToolTip("Min value")

				self.dlg.tableWidget.setItem(row,len(element[1])+1,item)
				self.dlg.tableWidget.setItem(row,len(element[1])+2,item2)


		self.createdOptions = True


	#Checks if there's an input shape or not
	def checkIfShape(self):
		
		nameShape = self.dlg.lineEdit_2.text()
		if nameShape is "":
			self.shapeBox = []
			return
		#if exists
		puntos = self.getShapefromLayer(nameShape)
		if puntos is None:
			#name doesn't match
			self.show_message("There is no Shape with name: "+nameShape+"\nPlease select a valid shape name or leave it blank for using all the tile")
		else:
			self.shapeBox= []
			for p in puntos:
				self.shapeBox.append([p.x(),p.y()])

	def checkIfCSV(self):
		if self.dlg.checkBox.checkState() == Qt.Checked:
			self.saveCSV = True
		else:
			self.saveCSV = False


	#it shows os file manager to choose a file.zip
	def select_input_file(self):
		filename = QFileDialog.getOpenFileName(self.dlg, "Select input file product Sentinel-2 ","", '*.zip')
		self.dlg.lineEdit.setText(str(filename))
		self.route_zip = str(filename[0])
		self.createDialog()


	def Select_Unselect(self):
		if self.createdOptions is True:
			for row in range(self.dlg.tableWidget.rowCount()):
				for column in range(1,self.dlg.tableWidget.columnCount()):
					try:
						item = self.dlg.tableWidget.item(row,column)
						if not item is None:
							if self.selectPhase is False:
								#select all
								item.setCheckState(Qt.Checked)
							else:
								#unselect all
								item.setCheckState(Qt.Unchecked)


					except:
						continue
		if self.selectPhase is False:
			self.selectPhase = True
		else:
			self.selectPhase = False



	#retrieve options cheked about Indexes
	def getChecked(self):
		checked_list = []
		for i in range(self.dlg.tableWidget.rowCount()):    
			indice = self.dlg.tableWidget.item(i, 0).text()
			opciones = []
			for j in range(1,self.dlg.tableWidget.columnCount()):
				item = self.dlg.tableWidget.item(i, j)
				if not item is None:
					if item.checkState() == Qt.Checked:
						opciones.append(self.dlg.tableWidget.item(i, j).text())

					#for CCCI min,max
					if indice == "CCCI":
						if "Max" in item.toolTip():
							value = self.dlg.tableWidget.item(i,j).text()
							try:
								self.CCCImax= float(value)
							except Exception:
								self.show_message("CCCI Max value is not supported")

						elif "Min" in item.toolTip():
							value = self.dlg.tableWidget.item(i,j).text()
							try:
								self.CCCImin= float(value)
							except Exception:
								self.show_message("CCCI Min value is not supported")
								

			if len(opciones) > 0:
				checked_list.append([indice, opciones])
		return checked_list

	#It shows a pop-up dialog
	def show_message(self, lis):
		#list of type ([el1,[op1,op2...opn]],...)
		# or string
		if type(lis) is str:
			QMessageBox.information(None, "Information", lis )

		elif type(lis) is list:
			el = ""
			for i in lis:
				el += i + '\n'
			QMessageBox.information(None, "Information", str(el) )


	###########  MY MAIN METHOD #############
	def calculate_indexes(self):
		list_indexAndOptions = self.getChecked()

		if len(list_indexAndOptions) == 0:
			self.show_message('You have to choice at least one Index.')
			return
		
		list_products = extract_data(self.route_zip)
		if len(list_products) == 0:
			self.show_message(self.route_zip+" is not a correct Zip file")


		self.show_message("The Calculation of all desired Vegetal Indexes could take up to some minutes. Close this message to continue.")
		

		puntos = getXYMinMax(self.shapeBox)
		Indexes = SpectralIndexes(list_products,puntos)
		for index in list_indexAndOptions:
			max_uint16 = 255

			if index[0] == 'OTCI':
				for item in index[1]:
					imagen, name = Indexes.OTCI(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,25,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == 'MCARI':
				for item in index[1]:
					imagen, name = Indexes.MCARI(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,0.5,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == 'IRECI':
				for item in index[1]:
					imagen, name = Indexes.IRECI(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,2.5,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "CCCI":
				for item in index[1]:
					if self.CCCImin is None or self.CCCImax is None:
						break
					imagen, name = Indexes.CCCI(1,item,self.CCCImin,self.CCCImax)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen, 1, max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "NDRE":
				for item in index[1]:
					imagen, name = Indexes.NDRE_1(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,1,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "MTCI":
				for item in index[1]:
					imagen, name = Indexes.MTCI(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,10,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "CI_redEdge":
				for item in index[1]:
					imagen, name = Indexes.CI_redEdge(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,2,max_uint16) 
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "CI_greenEdge":
				for item in index[1]:
					imagen, name = Indexes.CI_greenEdge(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,5,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "EVI":
				for item in index[1]:
					imagen, name = Indexes.EVI(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,2,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "NRERI":
				for item in index[1]:
					imagen, name = Indexes.NDVI_redEdge(item)#NRERI
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen, 10, max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "Color":
				for item in index[1]:
					imagen, name = Indexes.Color(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen, 1, max_uint16)
					dst_dir = Indexes.saveImages(imagen,3,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "NDVI705":
				for item in index[1]:
					imagen, name = Indexes.NDVI705(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,2,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "mNDVI705":
				for item in index[1]:
					imagen, name = Indexes.mNDVI705(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,2,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "NDI45":
				for item in index[1]:
					imagen, name = Indexes.NDI45(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,2,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "RDVI":
				for item in index[1]:
					imagen, name = Indexes.RDVI(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,2,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "TCARI":
				for item in index[1]:
					imagen, name = Indexes.TCARI(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,1,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "OSAVI":
				for item in index[1]:
					imagen, name = Indexes.OSAVI(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,2,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			elif index[0] == "TCARI/OSAVI":
				for item in index[1]:
					imagen, name = Indexes.TCARI_OSAVI(item)
					name = name+str(time.time())
					if self.saveCSV:
						Indexes.save2CSV(name,imagen)
					imagen = mapper(imagen,2,max_uint16)
					dst_dir = Indexes.saveImages(imagen,1,name)	
					iface.addRasterLayer(dst_dir+'.tif', name)
			else:
				continue

		self.show_message("All products have been created")



	def getShapefromLayer(self, name):
		project = QgsProject.instance()
		dicc = project.mapLayers()
		idn = None
		puntosResult = []
		for key in dicc:
			if name in key:
				idn = key
				break
		if idn is None:
			#not found that name in layers.
			return None

		vLayer = dicc[idn]
		puntos = vLayer.getFeatures()
		for p in puntos:
			puntosResult.append(p.geometry().asPoint())
		
		if len(puntosResult) == 0:
			return None
		else:
			return puntosResult


	#QGIS MAIN METHOD
	def run(self):
		"""Run method that performs all the real work"""
		# show the dialog
		self.dlg.show()
		# Run the dialog event loop
		result = self.dlg.exec_()
		# See if OK was pressed
		if result:
			#check if there's a shape
			self.checkIfShape()
			self.checkIfCSV()

			#If Shape is blank (all tile) or has points but not if we couldn't find any shape with that name 
			if not self.shapeBox is None:
				#calculate for the shape
				self.calculate_indexes()