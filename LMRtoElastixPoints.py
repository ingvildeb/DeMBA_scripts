# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 17:20:29 2023

@author: ingvieb
"""

import json

age = "P28"

mypath = r"Z:\HBP_Atlasing\Developmental_atlases\DeMBA_Developmental mouse brain atlas\DeMBA-v1\01_working-environment\01_Data\LMR_registrationData\\"

filename = "2023-09-06_LMR-curated-points_" + age + ".txt"

with open(mypath + filename) as file:
    openFile = json.load(file)
try:
    xyz_list = [(i["px"], i["py"], i["pz"]) for i in openFile]
except KeyError:
    raise Exception("you didnt set all the target points in LMR dummy")
    
with open(mypath + age + '_points.pts', 'w') as f:
    f.write("index")
    f.write('\n')    
    f.write(str(len(xyz_list)))
    f.write('\n')
    
    for point in xyz_list:
        
        f.write(f"{round(point[0])} {round(point[1])} {round(point[2])}\n")
        
    
xyz_list = [(i["x"], i["y"], i["z"]) for i in openFile]

with open(mypath + 'adult_points.pts', 'w') as f:
    f.write("index")
    f.write('\n')    
    f.write(str(len(xyz_list)))
    f.write('\n')
    
    for point in xyz_list:
        
        f.write(f"{round(point[0])} {round(point[1])} {round(point[2])}\n")
