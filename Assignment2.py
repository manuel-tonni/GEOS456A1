#-------------------------------------------------------------------------------
# Name:        Assignment 01
# Purpose:
#
# Author:      Emmanuel Perekeme Tonnipre (951186)
#
# Created:     20/05/2025
# Copyright:   (c) 951186 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os

# Defining all workspaces and spatial reference
in_workspace1 = r"C:\\Assignment01_Data\\communes"
in_workspace2 = r"C:\\Assignment01_Data\\reseau-cyclable-et-vert"
gdb = r"C:\\Assignment01_Data\\Toulouse.gdb"
sr = arcpy.SpatialReference("NTF (Paris) Sud France")

#Cleaning up the geodatabase by deleting all the features and tables in it
print("--- Cleaning Geodatabase ---")
arcpy.env.workspace = gdb
for fc in arcpy.ListFeatureClasses():
    arcpy.management.Delete(fc)

for table in arcpy.ListTables():
	arcpy.management.Delete(table)
print("=== Geodatabase Cleaned ===")

#Projecting all the shapefiles
arcpy.env.workspace = in_workspace1
fcList = arcpy.ListFeatureClasses()
for fc in fcList:
	print(f"Feature class in {in_workspace1} are : {fc}")
	folder, ext = os.path.splitext(fc)
	name = os.path.basename((folder)) #extracting the name of the shapefile
	newName = f"{gdb}\{name}" #adding the name of the shapefile to the path of the gdb so that the shapefile would be saved in the gdb

	print(f"=== Projecting {fc} to NTF (Paris) Sud France ===")
	print("--- Please Wait ---")
	project = arcpy.management.Project(fc,newName, sr) #Projecting the shapefiles
	print(f"=== {fc} was Projected to NTF (Paris) Sud France and was stored in {gdb} as {newName} ===")

arcpy.env.workspace = in_workspace2
fcList = arcpy.ListFeatureClasses()
for fc in fcList:
	print(f"Feature class in {in_workspace1} are : {fc}")
	folder, ext = os.path.splitext(fc)
	name = os.path.basename((folder)) #extracting the name of the shapefile
	newName = f"{gdb}\{name}" #adding the name of the shapefile to the path of the gdb so that the shapefile would be saved in the gdb

	print(f"=== Projecting {fc} to NTF (Paris) Sud France ===")
	print("--- Please Wait ---")
	project = arcpy.management.Project(fc,newName, sr) #Projecting the shapefiles
	print(f"=== {fc} was Projected to NTF (Paris) Sud France and was stored in {gdb} as {newName} ===")

# setting the workspace back to the gdb
arcpy.env.workspace = gdb
Ilayer = "communes"
distance = []
main = []

gdbFC = arcpy.ListFeatureClasses()
for fc in gdbFC:
	if fc != "communes": # to ensure that the communes layer is not used for any analysis
		folder, ext = os.path.splitext(fc)
		name = os.path.basename((folder))
		newName = f"{gdb}\{name}_Intersect" # extracting the name of the feature class and adding _Intersect to it

		print(f"=== Intersecting {fc} with {Ilayer} ===")
		print("--- Please Wait ---")
		intersect = arcpy.analysis.Intersect([fc,Ilayer],newName, 'ALL', '', 'line') #intersect each line feature class to the commues
		print(f"=== Sucessfully intersected {fc} with {Ilayer} ===")

		print(f"=== Calculating new field for {fc} ===")
		newFeild = arcpy.CalculateField_management(intersect, "KM_Distance", "!Shape_Length! / 1000", field_type="Float") #creates a new field and store the and converting the shape lenght to KM
		print(f"=== Successfully Created KM_Distance ===")

		print(f"=== Summarize Statistics tool is running based on the {intersect} layer ===")
		StatName = name+"_stats"
		stats = arcpy.Statistics_analysis(intersect, StatName,[["KM_Distance", 'SUM']], "libelle") #Summarize statistics based on the intersected area using sum operator on the newly calculated field and grouping them by the libelle
		print(f"=== Successfully Summarized {StatName} ===")

		print("=== Looking for top 3 commues ===")
		with arcpy.da.SearchCursor(StatName, ["SUM_KM_Distance","libelle"]) as cursor: #creates a curcor that is able to go through the rows in a layer or table
			for row in cursor: #iterates over every row in the StatName feature class
				distance.append(('layer= '+name, 'Distance= '+str(row[0]), 'Name of community= '+row[1])) #adds the records in the SUM_KM_Distance and libelle field to the distance list
			distance.sort(reverse=True) #sorts the distance list in descending order to find the top 3
			main.append(distance[:3]) #adds the top 3 to the main list
	else:
		pass
print("Here are the top 3 communities with the longest path")
print(main)











