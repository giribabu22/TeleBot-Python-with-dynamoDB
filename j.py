import  psutil

print ("battery charge left: " + str(psutil.sensors_battery()[0]) + "%")