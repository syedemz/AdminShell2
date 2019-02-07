"""
Denis March 2017
This function is used to create a string in the required format to control the robot
The first number is 18 which is identified by the robot that a web application is doing the control

The secound number can be 1, 2 or 3
1 identifies the command as a starting command, the following entries are will not be readed
2 identifies the command as a control command. The 6 entries after this nummer are important information for the control
3 identifies the command as a stop/ending command. This can be used as emergency button. Analog to numer 1 the following 6 entries are not used

The last six entries are information to control the robot. Data is provided via the web application and transformed within the following function
"""

def robot_control(status,b1,a1,a2,a3,c1,position_grab):
    PI=3.14159265359
    a1=round(a1*180/PI)
    a2=round(a2*180/PI)
    a3=round(a3*180/PI)
    b1=round(b1*180/PI)
    c1=round(c1*180/PI)
    position_grab=round(position_grab*180/PI)
    
    str_a1=str(a1)
    if (a1<100 and a1>9):
        str_a1="0"+str_a1
    if a1<10:
        str_a1="00"+str_a1
        
    str_a2=str(a2)
    if (a2<100 and a2>9):
        str_a2="0"+str_a2
    if a2<10:
        str_a2="00"+str_a2
        
    str_a3=str(a3)
    if (a3<100 and a3>9):
        str_a3="0"+str_a3
    if a3<10:
        str_a3="00"+str_a3
        
    str_b1=str(b1)
    if (b1<100 and b1>9):
        str_b1="0"+str_b1
    if b1<10:
        str_b1="00"+str_b1
        
    str_c1=str(c1)
    if (c1<100 and c1>9):
        str_c1="0"+str_c1
    if c1<10:
        str_c1="00"+str_c1
        
        
    str_position_grab=str(position_grab)
    if (position_grab<100 and position_grab>9):
        str_position_grab="0"+str_position_grab
    if position_grab<10:
        str_position_grab="00"+str_position_grab
    
        
    #command_robot="18 "+str(status)+" "+str(b1)+" "+str(a1)+" "+str(a2)+" "+str(a3)+" "+str(c1)+" "+str(position_grab)    
    command_robot="18 0"+str(status)+" "+str_b1+" "+str_a1+" "+str_a2+" "+str_a3+" "+str_c1+" "+str_position_grab
    return command_robot
    
"""
The returned command_robot string hast to be sent to the required program on the raspberry to control the robot.
"""