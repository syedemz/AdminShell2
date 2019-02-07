# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 21:02:16 2017

@author: Denis
"""

#### motion has 9 columns with angles, angle velocity and angle accelaration
simulink_robot_motion=[]
with open('C:\\Users\Denis\Desktop\matlab\simulink_robot_motion.txt',"r") as data_file:
    rows=0
    for line in data_file:
        rows=rows+1
    columns=len(line.split(","))
    simulink_robot_motion=[[0 for x in range(columns)] for y in range(rows)]
    i=0
    with open('C:\\Users\Denis\Desktop\matlab\simulink_robot_motion.txt',"r") as data_file:
        for line in data_file:
            current_line = line.split(",")
            current_line = list(map(float, current_line))
            simulink_robot_motion[i]=current_line
            i=i+1
             

            
### motor sensor data have 3 columns with motor torque of the respective 
simulink_robot_motor=[]
with open('C:\\Users\Denis\Desktop\matlab\sensor_data_motor.txt',"r") as data_file:
    rows=0
    for line in data_file:
        rows=rows+1
    columns=len(line.split(","))
    simulink_robot_motor=[[0 for x in range(columns)] for y in range(rows)]
    i=0
    with open('C:\\Users\Denis\Desktop\matlab\simulink_robot_motor.txt',"r") as data_file:
        for line in data_file:
            current_line = line.split(",")
            current_line = list(map(float, current_line))
            simulink_robot_motor[i]=current_line
            i=i+1
            
            
### motor sensor data of first motor: time and torque as columns
simulink_robot_motor1=[]
with open('C:\\Users\Denis\Desktop\matlab\motor_M1_sensor.txt',"r") as data_file:
    rows=0
    for line in data_file:
        rows=rows+1
    columns=len(line.split(","))
    simulink_robot_motor1=[[0 for x in range(columns)] for y in range(rows)]
    i=0
    with open('C:\\Users\Denis\Desktop\matlab\motor_M1_sensor.txt',"r") as data_file:
        for line in data_file:
            current_line = line.split(",")
            current_line = list(map(float, current_line))
            simulink_robot_motor1[i]=current_line
            i=i+1            

def import_sensor_data():
    simulink_robot_motor1=[]
    with open('C:\\Users\Denis\Desktop\matlab\motor_M1_sensor.txt',"r") as data_file:
        rows=0
        for line in data_file:
            rows=rows+1
        columns=len(line.split(","))
        simulink_robot_motor1=[[0 for x in range(columns)] for y in range(rows)]
        i=0
        with open('C:\\Users\Denis\Desktop\matlab\motor_M1_sensor.txt',"r") as data_file:
            for line in data_file:
                current_line = line.split(",")
                current_line = list(map(float, current_line))
                simulink_robot_motor1[i]=current_line
                i=i+1
                return (simulink_robot_motor1)
                
def get_matlab_sensor_data():
    results=[]
    with open('C:\\Users\Denis\Desktop\matlab\motor_M1_sensor.txt','r') as data_file:
        for line in data_file:
            current_line = line.split(',')
            current_line = list(map(float, current_line))
            results.append(current_line)
    return "hi"
                
                
