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
        roadl100 = traci.lane.getLength('297396114#4_0')
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
		print('Alternative route JALAN FLORA')
      	
      		
      	
      	
      	print '------------------------------------------------'

	#calculates traffic congestion at 300m
      	print(color.BLUE + color.BOLD + '300M RSU RANGE' + color.END)
      	roadl300 = traci.lane.getLength('297396114#3_0')+roadl100
      	print 'ROAD LENGTH \t\t\t:',roadl300
    	
     	num300 = traci.edge.getLastStepVehicleNumber('297396114#3')+vnumber100
    	if num300 == 0:
    		speed300 = 0
    	else:
    		if num300 != 0 and num100 ==0 :
    			speed300 = traci.edge.getLastStepMeanSpeed('297396114#3')
    		else:
        		speed300 = traci.edge.getLastStepMeanSpeed('297396114#4')+traci.edge.getLastStepMeanSpeed('297396114#3')
        		speed300 = speed300/2
        print 'AVERAGE SPEED AT 300M \t\t:',speed300
        
      	vnumber300 = traci.edge.getLastStepVehicleNumber('297396114#3')+vnumber100
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
      	
   
      	
      	with open('100m.csv', 'a') as file:
      		writer = csv.writer(file, delimiter = ',')
      		if (step % 20 == 0):
      			writer.writerow([step,vnumber100,speed100])
      	
      	  		      
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
