from sense_hat import SenseHat
from datetime import datetime

## sensor settings ##
FILENAME = ""
WRITE_FREQUENCY = 15
## methods ##

def file_setup(filename):
    header= ["temp_from_humidity","temp_from_pressure","humidity","pressure",
             "pitch","roll","yaw",
             "mag_x","mag_y","mag_z",
             "acc_x","acc_y","acc_z",
             "gyro_x","gryo_y","gyro_z",
             "timestamp"]
    with open(filename,"w") as f:
        f.write(",".join(str(value) for value in header)+ "\n")
def data_log():
    data_string = ",".join(str(value) for value in sensor_data)
    batch_data.append(data_string)

def get_sensor_data():
    sensor_data=[]

    sensor_data.append(sensor.get_temperature_from_humidity())
    sensor_data.append(sensor.get_temperature_from_pressure())
    sensor_data.append(sensor.get_humidity())
    sensor_data.append(sensor.get_pressure())
    
    orientation = sensor.get_orientation()
    yaw = orientation["yaw"]
    pitch = orientation["pitch"]
    roll = orientation["roll"]
    sensor_data.extend([pitch, roll, yaw])
    
    mag = sensor.get_compass_raw()
    mag_x = mag["x"]
    mag_y = mag["y"]
    mag_z = mag["z"]
    sensor_data.extend([mag_x, mag_y, mag_z])
    
    acc = sensor.get_accelerometer_raw()
    x = acc["x"]
    y = acc["y"]
    z = acc["z"]
    sensor_data.extend([x, y, z])
    
    gyro = sensor.get_gyroscope_raw()
    gyro_x = gyro["x"]
    gyro_y = gyro["y"]
    gyro_z = gyro["z"]
    sensor_data.extend([gyro_x, gyro_y, gyro_z])
    sensor_data.append(datetime.now())
    
    return sensor_data

## behavior ##

sensor = SenseHat()

batch_data = []

if FILENAME == "":
    filename = "flight-data-log-"+str(datetime.now())+".csv"
else:
    filename = FILENAME+"-"+str(datetime.now())+".csv"
file_setup(filename)
    

while True:
    sensor_data = get_sensor_data()
    data_log()
    
    if len(batch_data) >= WRITE_FREQUENCY:
        print("Log in progress...")
        with open(filename,"a") as f:
            for line in batch_data:
                f.write(line + "\n")
            batch_data = []