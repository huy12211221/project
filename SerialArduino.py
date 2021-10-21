
from sys import stdout
import serial
import time

class Serial_Arduino:
    def __init__(self,port,baud_rate):
        self.Arduino_data = serial.Serial(port,baud_rate)
        self.engle_current = 0
    def get_data(self):    
        try:
            """ while (self.Arduino_data.inWaiting() == 0): # Nếu chưa nhận được dữ liệu nào thì không làm gì cả
                pass """
            Data_byte = self.Arduino_data.readline() # Đọc dữ liệu từ Serial
            Data_string = Data_byte.decode("utf-8") # Chuyển dữ liệu Byte sang string
            data = Data_string.split(",")
            self.data_Humidity = data[0]
            self.data_Temperature = data[1]
            return self.data_Temperature,self.data_Humidity
        except IndexError:
            return 0,0
    def write_data(self,engle): #engle type int
        engle_string = str(engle)
        self.Arduino_data.write(engle_string.encode()) 
    def close_port(self):
        self.Arduino_data.close()
        

