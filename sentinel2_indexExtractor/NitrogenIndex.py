import sys
import zipfile
import os
import numpy as np
import gdal
import osr
from math import floor
from PyQt5.QtWidgets import QMessageBox


class Coordinates:
	def __init__(self, lista):
		self.ulx = lista[0]
		self.uly = lista[1]
		self.lrx = lista[2]
		self.lry = lista[3]

class SpectralIndexes:
	# PRE: image is np.array
	def __init__(self, route,puntos):
		self.B1_60 = route[0]  # 443nm 60m
		self.B2_10 = route[1]  # 490nm 10m
		self.B2_20 = route[2]  # 490nm 20m
		self.B2_60 = route[3]  # 490nm 60m
		self.B3_10 = route[4]  # 560nm 10m
		self.B3_20 = route[5]  # 560nm 20m
		self.B3_60 = route[6]  # 560nm 60m
		self.B4_10 = route[7]  # 665nm 10m
		self.B4_20 = route[8]  # 665nm 20m
		self.B4_60 = route[9]  # 665nm 60m
		self.B5_20 = route[10]  # 705nm 20m
		self.B5_60 = route[11]  # 705nm 60m
		self.B6_20 = route[12]  # 740nm 20m
		self.B6_60 = route[13]  # 740nm 60m
		self.B7_20 = route[14]  # 783nm 20m
		self.B7_60 = route[15]  # 783nm 60m
		self.B8_10 = route[16] # 842nm 10m
		self.B8a_20 = route[17]  # 865nm 20m
		self.B8a_60 = route[18]  # 865nm 60m
		self.B9_60 = route[19]  # 940nm 60m
		#self.B10 = route[9]  # 1375nm
		self.B11_20 = route[20]  # 1610nm 20m
		self.B11_60 = route[21]  # 1610nm 60m
		self.B12_20 = route[22]  # 2190nm 20m
		self.B12_60 = route[23]  # 2190nm 60m
		self.pwd = route[24] #PATH were we can work

		#Same for all
		self.metadata = None
		self.projection = None
		self.geoTransform = None

		self.puntos = puntos


	def OTCI(self, resolution):
		if '10' in resolution:
			Band04 = self.openImageAndSaveMetadata(self.B4_10,0,True)
			Band05 = self.openImageAndSaveMetadata(self.B5_20,2)
			Band06 = self.openImageAndSaveMetadata(self.B6_20,2)
			

			nombre = 'OTCI_10m'


		elif '20' in resolution:
			Band04 = self.openImageAndSaveMetadata(self.B4_20,0,True)
			Band05 = self.openImageAndSaveMetadata(self.B5_20,0)
			Band06 = self.openImageAndSaveMetadata(self.B6_20,0)

			nombre = 'OTCI_20m'
		else:
			Band04 = self.openImageAndSaveMetadata(self.B4_60,0,True)
			Band05 = self.openImageAndSaveMetadata(self.B5_60,0)
			Band06 = self.openImageAndSaveMetadata(self.B6_60,0)

			nombre = 'OTCI_60m'
		
		#METHOD	
		numerador = np.subtract(Band06,Band05)
		del Band06

		denominador = np.divide(np.add(Band04,Band05),2)#R681
		del Band04

		denominador = np.subtract(Band05, denominador)
		del Band05

		return np.divide(numerador, denominador), nombre

	def MCARI(self, resolution):
		if '10' in resolution:
			Band03 =self.openImageAndSaveMetadata(self.B3_10,0, True)
			Band04 =self.openImageAndSaveMetadata(self.B4_10,0)
			Band05 =self.openImageAndSaveMetadata(self.B5_20,2)



			nombre = 'MCARI_10m'


		elif '20' in resolution:
			Band03 =self.openImageAndSaveMetadata(self.B3_20,0, True)
			Band04 =self.openImageAndSaveMetadata(self.B4_20,0)
			Band05 =self.openImageAndSaveMetadata(self.B5_20,0)
			nombre = 'MCARI_20m'
		else:
			Band03 =self.openImageAndSaveMetadata(self.B3_60,0, True)
			Band04 =self.openImageAndSaveMetadata(self.B4_60,0)
			Band05 =self.openImageAndSaveMetadata(self.B5_60,0)
			nombre = 'MCARI_60m'

		#METHOD

		sustraendo = np.subtract(Band05,Band03)
		del Band03
		sustraendo = np.multiply(sustraendo, 0.2)
		sustraendo2 = np.divide(Band05,Band04)
		sustraendo = np.multiply(sustraendo,sustraendo2)
		del sustraendo2

		minuendo = np.subtract(Band05, Band04)
		del Band05
		del Band04

		return np.subtract(minuendo,sustraendo), nombre



	def IRECI(self,resolution):
		if '10' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_10, 0,True)
			Band05 =self.openImageAndSaveMetadata(self.B5_20,2)
			Band06 =self.openImageAndSaveMetadata(self.B6_20,2)
			Band07 =self.openImageAndSaveMetadata(self.B7_20,2)

			nombre = 'IRECI_10m'


		elif '20' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_20,0, True)
			Band05 =self.openImageAndSaveMetadata(self.B5_20,0)
			Band06 =self.openImageAndSaveMetadata(self.B6_20,0)
			Band07 =self.openImageAndSaveMetadata(self.B7_20,0)

			nombre = 'IRECI_20m'

		else:
			Band04 =self.openImageAndSaveMetadata(self.B4_60,0, True)
			Band05 =self.openImageAndSaveMetadata(self.B5_60,0)
			Band06 =self.openImageAndSaveMetadata(self.B6_60,0)
			Band07 =self.openImageAndSaveMetadata(self.B7_60,0)
			nombre = 'IRECI_60m'

		#METHOD

		numerador = np.multiply(np.subtract(Band07,Band04),Band06)
		del Band07
		del Band04
		del Band06

		
		return np.divide(numerador,Band05), nombre

	# CCCI index.
	# INPUT: N x N x 12BANDS Matrix (should be np array)
	# OUTPUT: matrix where items [0-1]
	def CCCI(self, NDRE ,resolution ,NDREmin=0.24 , NDREmax=0.62):
		if "20" in resolution:
			NDREresult, _ = self.NDRE_1(resolution)
			nombre = "CCCI_20m_interpolated"
		else:
			NDREresult, _ = self.NDRE_1(resolution)
			nombre = "CCCI_60m_interpolated"

		#NDREmin = np.min(NDREresult)
		NDREmin = 0
		#NDREmax = np.max(NDREresult)
		NDREresult = (NDREresult - NDREmin) / (NDREmax - NDREmin)

		return NDREresult, nombre
		
		#return result, nombre

	#NDRE NIR-RED/NIR+RED
	def NDRE_1(self, resolution):
		if '20' in resolution:
			Band05 =self.openImageAndSaveMetadata(self.B5_20,0, True)
			Band06=self.openImageAndSaveMetadata(self.B6_20,0)
			Band07 =self.openImageAndSaveMetadata(self.B7_20,0)

			nombre = "NDRE_20m_interpolated"

		else:#60
			Band05 =self.openImageAndSaveMetadata(self.B5_60,0, True)
			Band06=self.openImageAndSaveMetadata(self.B6_60,0)
			Band07 =self.openImageAndSaveMetadata(self.B7_60,0)

			nombre = "NDRE_60m_interpolated"

		#METHOD

		r720 = np.add(Band05,Band06)
		r720 = r720 / 2

		del Band05
		del Band06

		add = np.add(Band07,r720)
		diff = np.subtract(Band07, r720)

		del Band07
		del r720

		return np.divide(diff,add), nombre

	def MTCI(self, resolution):
		if '10' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_10,0, True)
			Band05=self.openImageAndSaveMetadata(self.B5_20,2)
			Band06 =self.openImageAndSaveMetadata(self.B6_20,2)

			nombre = "MTCI_10m"

		elif '20' in resolution:#60
			Band04 =self.openImageAndSaveMetadata(self.B4_20, 0,True)
			Band05=self.openImageAndSaveMetadata(self.B5_20,0)
			Band06 =self.openImageAndSaveMetadata(self.B6_20,0)

			nombre = "MTCI_20m"

		else:
			Band04 =self.openImageAndSaveMetadata(self.B4_60,0, True)
			Band05=self.openImageAndSaveMetadata(self.B5_60,0)
			Band06 =self.openImageAndSaveMetadata(self.B6_60,0)

			nombre = "MTCI_60m"
			
		#METHOD

		numerador = np.subtract(Band06, Band05)
		del Band06
		denominador = np.subtract(Band05, Band04)
		del Band05
		del Band04

		return np.divide(numerador, denominador), nombre




	#CI_redEdge = (R780/R705) -1
	def CI_redEdge(self, resolution):
		if "20" in resolution:
			Band05 =self.openImageAndSaveMetadata(self.B5_20,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_20,0)

			nombre = "ChlorophyllIndex_RedEdge_20m"

		else:
			Band05 =self.openImageAndSaveMetadata(self.B5_60,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_60,0)

			nombre = "ChlorophyllIndex_RedEdge_60m"

		#METHOD

		fraction = np.divide(Band07,Band05)
		del Band07
		del Band05

		return fraction -1, nombre

	def CI_greenEdge(self, resolution):
		if "10" in resolution:
			Band03 =self.openImageAndSaveMetadata(self.B3_10,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_20,2)

			nombre = "ChlorophyllIndex_GreenEdge_10m"
			

		elif "20" in resolution:
			Band03 =self.openImageAndSaveMetadata(self.B3_20,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_20,0)


			nombre = "ChlorophyllIndex_GreenEdge_20m"
		else:
			Band03 =self.openImageAndSaveMetadata(self.B3_60,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_60,0)

			nombre = "ChlorophyllIndex_GreenEdge_60m"

		#METHOD

		return np.subtract(np.divide(Band07,Band03),1), nombre


	#Enhanced Vegetation Index EVI
	#            2.5* (B8-B4)
	# EVI =  ---------------------
	#        (B8 +6B4 - 7.5B2 + 1)

	def EVI(self, resolution):
		if '10' in resolution:
			Band02 =self.openImageAndSaveMetadata(self.B2_10,0, True)
			Band04=self.openImageAndSaveMetadata(self.B4_10,0)
			Band08 =self.openImageAndSaveMetadata(self.B8_10,0)

			nombre = "EVI_10m"
		elif '20' in resolution:
			Band02 =self.openImageAndSaveMetadata(self.B2_20, 0,True)
			Band04=self.openImageAndSaveMetadata(self.B4_20,0)
			Band08 =self.openImageAndSaveMetadata(self.B8a_20,0)

			nombre = "EVI_20m"

		else:
			Band02 =self.openImageAndSaveMetadata(self.B2_60,0, True)
			Band04=self.openImageAndSaveMetadata(self.B4_60,0)
			Band08 =self.openImageAndSaveMetadata(self.B8a_60,0)

			nombre = "EVI_60m"

		#METHOD

		divisor = np.add(np.add(Band08,np.multiply(6,Band04)), 1)
		#divisor = np.add(np.add(Band08,np.multiply(Band04,2.4)), 1)
		numerador = np.multiply(np.subtract(Band08, Band04),2.5)
		del Band08
		del Band04
		divisor = np.subtract(divisor, np.multiply(7.5, Band02))

		return np.divide(numerador, divisor), nombre


	def NDVI_redEdge(self, resolution):
		if '10' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_10,0, True)
			Band05=self.openImageAndSaveMetadata(self.B5_20,2)
			Band06 =self.openImageAndSaveMetadata(self.B6_20,2)
			Band07 =self.openImageAndSaveMetadata(self.B7_20,2)

			nombre ="NRERI_10m"

		elif '20' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_20, 0,True)
			Band05=self.openImageAndSaveMetadata(self.B5_20,0)
			Band06 =self.openImageAndSaveMetadata(self.B6_20,0)
			Band07 =self.openImageAndSaveMetadata(self.B7_20,0)

			nombre ="NRERI_20m"
		else:
			Band04 =self.openImageAndSaveMetadata(self.B4_60, 0,True)
			Band05=self.openImageAndSaveMetadata(self.B5_60,0)
			Band06 =self.openImageAndSaveMetadata(self.B6_60,0)
			Band07 =self.openImageAndSaveMetadata(self.B7_60,0)

			nombre ="NRERI_60m"

		#METHOD

		r720 = np.divide(np.add(Band05,Band06),2)
		del Band05
		del Band06

		numerador = np.subtract(Band07, r720)
		del r720
		denominador = np.subtract(Band07, Band04)
		del Band07
		del Band04

		return np.divide(numerador,denominador), nombre


	def Color(self, resolution):
		if '10' in resolution:
			Band02 =self.openImageAndSaveMetadata(self.B2_10, 0,True)
			Band03=self.openImageAndSaveMetadata(self.B3_10,0)
			Band04 =self.openImageAndSaveMetadata(self.B4_10,0)


			nombre = "Color_10m"
		elif '20' in resolution:
			Band02 =self.openImageAndSaveMetadata(self.B2_20, 0,True)
			Band03=self.openImageAndSaveMetadata(self.B3_20,0)
			Band04 =self.openImageAndSaveMetadata(self.B4_20,0)


			nombre = "Color_20m"
		else:
			Band02 =self.openImageAndSaveMetadata(self.B2_60, 0,True)
			Band03=self.openImageAndSaveMetadata(self.B3_60,0)
			Band04 =self.openImageAndSaveMetadata(self.B4_60,0)

			nombre= "Color_60m"

		
		return np.array([Band04, Band03, Band02]), nombre


	#NVDI705 = (B6-B5)/(B6+B5-2*B1)
	def NDVI705(self, resolution):
		if '20' in resolution:
			Band05 =self.openImageAndSaveMetadata(self.B5_20,0, True)
			Band06=self.openImageAndSaveMetadata(self.B6_20,0)

			nombre = "NDVI705_20m"

		else:
			Band05 =self.openImageAndSaveMetadata(self.B5_60,0, True)
			Band06=self.openImageAndSaveMetadata(self.B6_60,0)

			nombre = "NDVI705_60m"

		#METHOD

		numerador = np.subtract(Band06, Band05)
		divisor = np.add(Band06, Band05)
		del Band05
		del Band06

		return np.divide(numerador, divisor), nombre

	def mNDVI705(self, resolution):
		if '20' in resolution:
			Band05 =self.openImageAndSaveMetadata(self.B5_20,0, True)
			Band06=self.openImageAndSaveMetadata(self.B6_20,0)
			Band01 =self.openImageAndSaveMetadata(self.B1_60,3)
			
			nombre = "mNDVI705_20m"

		else:
			Band05 =self.openImageAndSaveMetadata(self.B5_60,0, True)
			Band06=self.openImageAndSaveMetadata(self.B6_60,0)
			Band01 =self.openImageAndSaveMetadata(self.B1_60,0)

			nombre = "mNDVI705_60m"

		#METHOD

		numerador = np.subtract(Band06, Band05)
		divisor = np.add(Band06, Band05)
		divisor = np.subtract(divisor,np.multiply(2,Band01))
		del Band05
		del Band06
		del Band01

		return np.divide(numerador, divisor), nombre

	def NDI45(self, resolution):
		if '10' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_10,0, True)
			Band05=self.openImageAndSaveMetadata(self.B5_20,2)



			nombre = "NDI45_10m"

		elif '20' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_20,0, True)
			Band05=self.openImageAndSaveMetadata(self.B5_20,0)

			nombre = "NDI45_20m"

		else:
			Band04 =self.openImageAndSaveMetadata(self.B4_60,0, True)
			Band05=self.openImageAndSaveMetadata(self.B5_60,0)
			nombre = "NDI45_60m"

		#METHOD

		numerador = np.subtract(Band05, Band04)
		denominador = np.add(Band05, Band04)

		del Band05
		del Band04

		return np.divide(numerador, denominador), nombre

	def RDVI(self, resolution):
		if '10' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_10,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_20,2)
						
			nombre = "RDVI_10m"
		elif '20' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_20,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_20,0)

			nombre = "RDVI_20m"
		else:
			Band04 =self.openImageAndSaveMetadata(self.B4_60,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_60,0)

			nombre = "RDVI_60m"

		#METHOD

		resultado = np.subtract(Band07, Band04)

		return np.divide(resultado, np.sqrt(resultado)), nombre



	def TCARI(self, resolution):
		if '10' in resolution:
			Band03 =self.openImageAndSaveMetadata(self.B3_10,0, True)
			Band04=self.openImageAndSaveMetadata(self.B4_10,0)
			Band05 =self.openImageAndSaveMetadata(self.B5_20,2)
			
			nombre = "TCARI_10m"
		
		elif '20' in resolution:
			Band03 =self.openImageAndSaveMetadata(self.B3_20,0, True)
			Band04=self.openImageAndSaveMetadata(self.B4_20,0)
			Band05 =self.openImageAndSaveMetadata(self.B5_20,0)

			nombre = "TCARI_20m"
		else:
			Band03 =self.openImageAndSaveMetadata(self.B3_60, 0,True)
			Band04=self.openImageAndSaveMetadata(self.B4_60,0)
			Band05 =self.openImageAndSaveMetadata(self.B5_60,0)

			nombre = "TCARI_60m"
		
		#METHOD

		minuendo = np.subtract(Band05, Band04)
		sustraendo = np.multiply(np.multiply(np.subtract(Band05,Band03),np.divide(Band05,Band04)),0.2)
		del Band05
		del Band04
		del Band03

		numerador = np.subtract(minuendo,sustraendo)
		del minuendo
		del sustraendo
		return np.multiply(numerador,3), nombre

	def OSAVI(self, resolution):
		if '10' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_10,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_20,2)

			nombre = "OSAVI_10m"
		elif '20' in resolution:
			Band04 =self.openImageAndSaveMetadata(self.B4_20, 0,True)
			Band07=self.openImageAndSaveMetadata(self.B7_20,0)
			
			nombre = "OSAVI_20m"
		else:
			Band04 =self.openImageAndSaveMetadata(self.B4_60,0, True)
			Band07=self.openImageAndSaveMetadata(self.B7_60,0)

			nombre = "OSAVI_60m"

		#METHOD

		numerador = np.multiply(1.16, np.subtract(Band07, Band04))
		denominador = np.add(0.16,np.add(Band07,Band04))
		del Band07
		del Band04

		return np.divide(numerador, denominador), nombre

	def TCARI_OSAVI(self, resolution):
		if '10' in resolution:
			tcari, _ = self.TCARI('10')
			osavi, _ = self.OSAVI('10')

			nombre = "TCARI_div_OSAVI_10m"
		elif '20' in resolution:
			tcari, _ = self.TCARI('20')
			osavi, _ = self.OSAVI('20')
			
			nombre = "TCARI_div_OSAVI_20m"
		else:
			tcari, _ = self.TCARI('60')
			osavi, _ = self.OSAVI('60')

			nombre = "TCARI_div_OSAVI_60m"

		return np.divide(tcari, osavi), nombre


	#SaveMetadata has to be True at the first Band opened in a method. So self.ymin, self.xmin...etc not raise Exceptions due to its inexistence
	def openImageAndSaveMetadata(self, image_name,resizeValue,saveMetadata=False):
		ds = gdal.Open(image_name, gdal.GA_ReadOnly)
		rb = ds.GetRasterBand(1)
		Band = rb.ReadAsArray()
		if saveMetadata:
			self.saveMetadata(ds)
		del ds
		del rb

		if resizeValue > 0:
			Band = Band.repeat(resizeValue, axis=0).repeat(resizeValue, axis=1)

		Band = Band[self.ymin: self.ymax,self.xmin :self.xmax]
		Band[Band>4095]= 0
		#Get reflectance normaliced
		Band = mapper(Band,4095,1)

		return Band


	def save2CSV(self,name,im):
		try:
			dire = self.pwd +"_NitrogenMaps"
			os.mkdir(dire)
		except OSError:
			#Directory already exists
			pass
		
		output_file = dire+"/"+name+'.csv'

		with open(output_file, 'w') as f:
			its = range(len(im))
			for i in its:
				for j in its:
					Cx,Cy = Pix2Coord(self.geoTransform,i,j)
					#show_message(str(Cx)+"\t"+str(Cy)+"\n"+str(i)+"\t"+str(j))
					f.write(str(Cx)+"\t"+","+"\t"+str(Cy)+"\t"+","+"\t"+str(im[i][j])+"\n")
		

	def saveImages(self, im, numberOfBands,title):
		e_type=gdal.GDT_Byte
		#e_type=gdal.GDT_UInt16
		try:
			dire = self.pwd +"_NitrogenMaps"
			os.mkdir(dire)
		except OSError:
			#Directory already exists
			pass

		output_file = dire+"/"+title
		if numberOfBands == 1:
			output_raster = gdal.GetDriverByName('GTiff').Create(output_file+'.tif', xsize=len(im[0]), ysize=len(im), bands=1, eType=e_type)
			output_raster.SetMetadata(self.metadata)
			output_raster.SetProjection(self.projection)
			output_raster.SetGeoTransform(self.geoTransform)
			output_raster.GetRasterBand(1).WriteArray(im)   # Writes my array to the raster
				
		else:
			output_raster = gdal.GetDriverByName('GTiff').Create(output_file+'.tif', xsize=len(im[0][0]), ysize=len(im[0]), bands=3, eType=gdal.GDT_UInt16)
			output_raster.SetMetadata(self.metadata)
			output_raster.SetProjection(self.projection)
			output_raster.SetGeoTransform(self.geoTransform)
			output_raster.GetRasterBand(1).WriteArray(im[0])   # Writes my array to the raster
			output_raster.GetRasterBand(2).WriteArray(im[1])   # Writes my array to the raster
			output_raster.GetRasterBand(3).WriteArray(im[2])   # Writes my array to the raster

		return output_file

	def saveMetadata(self, ds):
		self.metadata = ds.GetMetadata()
		self.projection = ds.GetProjection()
		self.geoTransform = ds.GetGeoTransform()

		#Establish points for indexes
		#If no shape selected
		if self.puntos is None:
			self.xmin=0
			self.xmax=-1
			self.ymin=0
			self.ymax=-1
		else:
			#Transform coordinates to points
			rb = ds.GetRasterBand(1)
			Band = rb.ReadAsArray()
			lenghtBigFrame = len(Band)
			del rb
			del Band
			coordinatesBigFrame = self.totalCoordinates(lenghtBigFrame)
			self.xmin, self.ymin = coord2pix(lenghtBigFrame, coordinatesBigFrame,self.puntos.ulx,self.puntos.uly)
			self.xmax, self.ymax = coord2pix(lenghtBigFrame, coordinatesBigFrame,self.puntos.lrx,self.puntos.lry)


			self.geoTransform = (self.puntos.ulx, self.geoTransform[1],self.geoTransform[2],self.puntos.uly,self.geoTransform[4],self.geoTransform[5])
			#show_message(str(self.puntos.ulx)+' '+str(self.puntos.uly)+'\n'+str(self.puntos.lrx)+' '+str(self.puntos.lry)+
			#	'\n\n'+str(self.xmin)+' '+str(self.ymin)+'\n'+str(self.xmax)+' '+str(self.ymax))


	
	#Returns coordinates from original image (big frame)
	def totalCoordinates(self,RasterSize):
		ulx, xres, xskew, uly, yskew, yres  = self.geoTransform
		lrx = ulx + (RasterSize * xres)
		lry = uly + (RasterSize * yres)
		return Coordinates([ulx,uly,lrx,lry])



#Calculates coordinates CX and CY for PixelX and PixelY
def Pix2Coord(geoTransform, Px,Py):
	razon = geoTransform[1]#resolution of the rasterBand
	ulCx = geoTransform[0]
	ulCy = geoTransform[3]

	#As UTM 0,0 is in lower-left corner from the tile
	return (Px*razon)+ulCx, ulCy-(Py*razon)

#Calculates PixelX and PixelY for Coordinates Cx and Cy
def coord2pix(lenghtBigFrame,coordinatesBigFrame,Cx,Cy):
	#Are Cx and Cy into the bigFrame?
	#ulpt = [coordinatesBigFrame.ulx,coordinatesBigFrame.uly]
	#urpt = [coordinatesBigFrame.lrx,coordinatesBigFrame.uly]
	#llpt = [coordinatesBigFrame.ulx,coordinatesBigFrame.lry]
	#lrpt = [coordinatesBigFrame.lrx,coordinatesBigFrame.lry]
	#if inBox([Cx,Cy],[ulpt,urpt,llpt,lrpt]) is False:
	#	return None

	#razon is mts/pix (as coordinates is given in mts)
	razon = (coordinatesBigFrame.lrx-coordinatesBigFrame.ulx)/lenghtBigFrame
	return int((Cx-coordinatesBigFrame.ulx)/razon), int((coordinatesBigFrame.uly-Cy)/razon)

#Given a list of points, get ulx,uly,lrx,lry
def getXYMinMax(lista):
	if len(lista)>2:
		ulx=min(lista, key = lambda elem: elem[0])[0]
		uly=max(lista, key = lambda elem: elem[1])[1]
		lrx=max(lista, key = lambda elem: elem[0])[0]
		lry=min(lista, key = lambda elem: elem[1])[1]
		return Coordinates([ulx,uly,lrx,lry])
	else:
		return None



def mapper(matrix,oldRange,NewRange=65535):
	factor = NewRange / oldRange
	return np.multiply(matrix, factor)

def extract_data(route_zip):

	if not zipfile.is_zipfile(route_zip):
		return 

	zip_ref = zipfile.ZipFile(route_zip)
	route_dest = route_zip.split("/")
	route_dest = route_dest[0:-1]#same location as original
	route_dest = "/".join(route_dest)

	#TODO uncomment/coment that line
	zip_ref.extractall(route_dest)

	files = zip_ref.namelist()
	#bands avaibles on Sentinel-2
	bands_list_extension = ["B01_60m",
							"B02_10m","B02_20m","B02_60m",
							"B03_10m","B03_20m","B03_60m",
							"B04_10m","B04_20m","B04_60m",
							"B05_20m","B05_60m",
							"B06_20m","B06_60m",
							"B07_20m","B07_60m",
							"B08_10m","B8A_20m","B8A_60m",
							"B09_60m",
							"B11_20m","B11_60m",
							"B12_20m","B12_60m"]
	bands_files = ["" for a in range(len(bands_list_extension))]#Initialise the list
	for band in bands_list_extension:
		for f in files:
			if str(band) in str(f) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.jp2')):
				archive = route_dest+"/"+f
				bands_files[band_index(band,bands_list_extension)] = archive

	zip_ref.close()
	if len(bands_files) != len(bands_list_extension):
		print("An error have occurred while finding spectral images format")
		return
	bands_files.append(getNamePackage(route_zip))
	return bands_files




def band_index(band,bands_list_extension):
	return bands_list_extension.index(band)

def getNamePackage(route):
	st = route.split("/")
	st_end = st[-1].split(".")

	return "/".join(st[0:-1])+"/"+st_end[0]


# Area signada del triangulo determinado por tres puntos a,b,c. La salida es el valor numerico del area signada del triangulo abc.
def sarea(a,b,c):#OK
	return (((b[0]-a[0])*(c[1]-a[1]))-((b[1]-a[1])*(c[0]-a[0])))/2 #La salida es positiva si C esta a la izq del segmento

# Test punto en segmento (p es un punto [x,y] y s es un segmento determinado por sus extremos [[a1,a2],[b1,b2]]. La salida es True o False.
def inSegment(p,s):#OK
	if ( sarea(p,s[0],s[1]) != 0):  #Si estan en la misma recta dara 0
		return False
	elif ( s[0][0] > s[1][0] ): #Conpruebo si C esta antes que B es decir, pertenece al segmento
			return s[0][0] >= p[0] and s[1][0] <= p[0]
	else:
			return s[0][0] <= p[0] and s[1][0] >= p[0]

# Test punto en triangulo. Entrada un punto p=[x,y] y un triangulo dado por una lista con sus tres vertices. Salida True o False.
def inTriangle(p,t):#OK
	ABP = sarea(t[0],t[1],p)
	BCP = sarea(t[1],t[2],p)
	CAP = sarea(t[2],t[0],p)

	#print(ABP, BCP, CAP)
	if ( ABP == 0 and BCP == 0 and CAP == 0):
		m = min(t[0],t[1],t[2])
		ma = max(t[0],t[1],t[2])
		return inSegment(p, [m ,ma])

	elif ( ABP <= 0 and BCP <= 0 and CAP <= 0):
		return True
	elif (ABP >= 0 and BCP >= 0 and CAP >= 0):
		return True
	else:
		return False
def inBox(pt, polygon):
	pol = polygon[:]
	while len(pol) > 3:
		idx = floor(len(pol)/2)
		sa = sarea(pol[0],pol[idx],pt)
		if sa == 0:
			return inSegment(pt,[pol[0],pol[idx]])
		elif sa < 0:
			pol = pol[:idx+1]
		else:
			pol = pol[idx-1:]

	return inTriangle(pt,pol)

#It shows a pop-up dialog
def show_message(lis):
	#lista del tipo ([el1,[op1,op2...opn]],...)
	# o un string

	if type(lis) is str:
		QMessageBox.information(None, "Information", lis )

	elif type(lis) is list:
		el = ""
		for i in lis:
			el += i + '\n'# +" "+ " ".join(map(str,i[1]))+"\n"
		QMessageBox.information(None, "Information", str(el) )