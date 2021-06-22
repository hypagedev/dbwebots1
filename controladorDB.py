from controller import Robot, Camera
import cv2

def run_robot(robot):
    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())
    izq_motor = robot.getDevice('left wheel motor')
    der_motor = robot.getDevice('right wheel motor')    
    izq_motor.setPosition(float('inf'))
    izq_motor.setVelocity(0.0)
    der_motor.setPosition(float('inf'))
    der_motor.setVelocity(0.0)  

    sensor_izq_frente = robot.getDevice('ground front left infrared sensor')
    sensor_izq_frente.enable(timestep)
    sensor_der_frente = robot.getDevice('ground front right infrared sensor')
    sensor_der_frente.enable(timestep)
    # Main loop:
    max_speed = 3.14
    count = 1
    data_file = open("data.csv","w" )
    data_file.write("izq, der, id, img\n")
    y_file = open("ydb.csv","w")
    y_file.write("out\n")
    
    camara = robot.getDevice('camera')
    Camera.enable(camara,timestep)
    cv2.startWindowThread()
    #cv2.namedWindow('original')
    cv2.namedWindow('original')
    
    while robot.step(timestep) != -1:
        nameimg = "img/"+str(count)+".png"
        Camera.getImage(camara)
        Camera.saveImage(camara,nameimg,1)
        img = cv2.imread(nameimg)
        cv2.imshow('original',img)
        izq_value = sensor_izq_frente.getValue()
        der_value = sensor_der_frente.getValue()
        
        data_file.write(str(izq_value/1023.0)+", ")
        data_file.write(str(der_value/1023.0)+", ")
        data_file.write(str(count)+ ", "+nameimg)
        data_file.write("\n")
        print('--------------------------')
        print('sensor izq frente: {}'.format(izq_value))
        print('sensor der frente: {}'.format(der_value))
        
        linea_izq = izq_value < 400
        linea_der = der_value < 400
        izq_vel = max_speed
        der_vel = max_speed
        
        if (linea_izq and linea_der):
            print('Defrente', end=' ')
            y_file.write("F")
            izq_vel = max_speed
            der_vel = max_speed            
        if( linea_izq and not linea_der):
            print('A la izquierda', end=' ')
            y_file.write("I")
            der_vel = max_speed
            izq_vel = -max_speed/8        
        if( not linea_izq and linea_der):
            print('A la derecha', end=' ')
            y_file.write("D")
            der_vel = -max_speed/8
            izq_vel = max_speed        
        if( not linea_izq and not linea_der):
            print('A la derecha rapido', end=' ')
            y_file.write("R")
            der_vel = max_speed
            izq_vel = -max_speed
        print()
        y_file.write("\n")    
        izq_motor.setVelocity(izq_vel)
        der_motor.setVelocity(der_vel)
        count+=1
        cv2.waitKey(2)
        
    y_file.close()
    data_file.close()

if __name__ == "__main__":
    mirobot = Robot()
    run_robot(mirobot)
