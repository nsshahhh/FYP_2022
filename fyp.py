#!/usr/bin/env python

import os
import sys
import optparse
import tkMessageBox
import csv

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
    
# contains TraCI control loop
def run():
    step = 0
    
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        os.system('clear')
        step += 1
        
        #calculates traffic congestion at 100m
        print(color.BLUE + color.BOLD + '100M RSU RANGE' + color.END)
        roadl100 = traci.lane.getLength('297396114#4')
    	print 'ROAD LENGTH \t\t\t:',roadl100
    	
    	num100 = traci.edge.getLastStepVehicleNumber('297396114#4')
    	if num100 == 0:
    		speed100 = 0
    	else:	
        	speed100 = traci.edge.getLastStepMeanSpeed('297396114#4')
        print 'AVERAGE SPEED AT 100M \t\t:',speed100
        
      	vnumber100 = traci.edge.getLastStepVehicleNumber('297396114#4')
      	print 'NUMBER OF VEHICLES AT 100M \t:',vnumber100
      	
      	tcar100 = roadl100/5.1
      	tcar100 = (tcar100*3)
      	tcar100 = tcar100*0.8
      	print 'MAXIMUM CAPACITY OF ROAD \t:',tcar100
      	
      	if vnumber100 > tcar100 and speed100 < 5:
      		print(color.RED + color.BOLD + 'TRAFFIC CONGESTION DETECTED !' + color.END)
      		print('SENT TRAFFIC CONGESTION ALERT TO ALL CARS')
      		
      	else:
      		print('NO TRAFFIC CONGESTION AT 100M')
      	
      		
      	
      	
      	print '------------------------------------------------'
      	
      	#calculates traffic congestion at 300m
      	print(color.BLUE + color.BOLD + '300M RSU RANGE' + color.END)
      	roadl300 = traci.lane.getLength('297396114#4')+roadl100
      	print 'ROAD LENGTH \t\t\t:',roadl300
    	
     	num300 = traci.edge.getLastStepVehicleNumber('297396114#4')+vnumber100
    	if num300 == 0:
    		speed300 = 0
    	else:
    		if num300 != 0 and num100 ==0 :
    			speed300 = traci.edge.getLastStepMeanSpeed('297396114')
    		else:
        		speed300 = traci.edge.getLastStepMeanSpeed('297396114')+traci.edge.getLastStepMeanSpeed('297396114')
        		speed300 = speed300/2
        print 'AVERAGE SPEED AT 300M \t\t:',speed300
        
      	vnumber300 = traci.edge.getLastStepVehicleNumber('297396114#4')+vnumber100
      	print 'NUMBER OF VEHICLES AT 300M \t:',vnumber300
      	
      	tcar300 = roadl300/5.1
      	tcar300 = (tcar300*3)
      	tcar300 = tcar300*0.8
      	print 'MAXIMUM CAPACITY OF ROAD \t:',tcar300
      	
      	if vnumber300 > tcar300 and speed300 < 5:
      		print(color.RED + color.BOLD + 'TRAFFIC CONGESTION DETECTED !' + color.END)
      		print('SENT TRAFFIC CONGESTION ALERT TO ALL CARS')
      		
      	else:
      		print('NO TRAFFIC CONGESTION AT 300M')
      	
      	print '------------------------------------------------'
      	
      	#calculates traffic congestion at 500m
      	print(color.BLUE + color.BOLD + '500M RSU RANGE' + color.END)
      	roadl500 = traci.lane.getLength('297396114')+roadl100+roadl300
      	print 'ROAD LENGTH \t\t\t:',roadl500
    	
        num500 = traci.edge.getLastStepVehicleNumber('297396114')+vnumber100+vnumber300
    	if num500 == 0:
    		speed500 = 0
    	else:
    		if num500 != 0 and num300 == 0 and num100 == 0:
        		speed500 = traci.edge.getLastStepMeanSpeed('297396114')
        	elif num500 != 0 and num300 != 0 and num100 == 0:
        		speed500 = traci.edge.getLastStepMeanSpeed('297396114')+traci.edge.getLastStepMeanSpeed('297396114')
        		speed500 = speed500/2
        	else:
        		speed500 = traci.edge.getLastStepMeanSpeed('297396114')+traci.edge.getLastStepMeanSpeed('297396114')+traci.edge.getLastStepMeanSpeed('297396114')
        		speed500 = speed500/3
        print 'AVERAGE SPEED AT 500M \t\t:',speed500
        
      	vnumber500 = traci.edge.getLastStepVehicleNumber('297396114')+vnumber100+vnumber300
      	print 'NUMBER OF VEHICLES AT 500M \t:',vnumber500 
      	
      	tcar500 = roadl500/5.1
      	tcar500 = (tcar500*3)
      	tcar500 = tcar500*0.8
      	print 'MAXIMUM CAPACITY OF ROAD \t:',tcar500
      	
      	if vnumber500 > tcar500 and speed500 < 5:
      		print(color.RED + color.BOLD + 'TRAFFIC CONGESTION DETECTED !' + color.END)
      		print('SENT TRAFFIC CONGESTION ALERT TO ALL CARS')
      		
      	else:
      		print('NO TRAFFIC CONGESTION AT 500M')
      	
      	print '------------------------------------------------'
      	
      	position = traci.vehicle.getIDList
      	print(position)
      	
      	with open('100m.csv', 'a') as file:
      		writer = csv.writer(file, delimiter = ',')
      		if (step % 20 == 0):
      			writer.writerow([step,vnumber100,speed100])
      	
      	with open('300m.csv', 'a') as file:
      		writer = csv.writer(file, delimiter = ',')
      		if (step % 20 == 0):
      			writer.writerow([step,vnumber300,speed300])
      			
      	with open('500m.csv', 'a') as file:
      		writer = csv.writer(file, delimiter = ',')
      		if (step % 10 == 0):
      			writer.writerow([step,vnumber500,speed500])
      	
      	  		      
    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:

	sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

     # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "fyp.sumo.cfg",
                             "--tripinfo-output", "tripinfo.xml"])
    run()
