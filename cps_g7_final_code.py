#Importing Required Libraries
import spidev
import time
import os
import Adafruit_DHT
import RPi.GPIO as GPIO
import mysql.connector as connector

#Defining parameters
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
channel = 0

def get_soil_moisture_percentage():
    adc_data = spi.xfer2([1, 8+channel<<4, 0])
    max_value = 1000
    adc_value = ((adc_data[1] & 3) << 8) + adc_data[2]
    if(adc_value > max_value):
        max_value = adc_value
    moisture_percentage = (max_value - adc_value)/max_value * 100.0
    return moisture_percentage

def get_temperature_humudity_values(): 
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 25
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return humidity, temperature
    
def trigger_water_pump(seconds=2):
    relay_pin = 18
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)
    GPIO.output(relay_pin, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.output(relay_pin, GPIO.LOW)
    GPIO.cleanup() 

def push_sensor_data():
    connection = connector.connect(
        host='',
        user='',
        password='',
        database=''
    )
    cursor = connection.cursor()
    soil_moisture = get_soil_moisture_percentage()
    humidity, temperature = get_temperature_humudity_values()
    
    if soil_moisture == None:
        soil_moisture = -1.0
    if humidity == None:
        humidity = -1.0
    if temperature == None:
        temperature = -1.0
    
    cursor.execute(f"INSERT INTO g7_plant_sensor_data (soil_moisture, temperature, humidity) VALUES ({soil_moisture}, {temperature}, {humidity})")
    cursor.execute("COMMIT")
    cursor.close()
    connection.close()
    #print("Latest Data Inserted!")

def fetch_latest_sensor_data():
    connection = connector.connect(
        host='',
        user='',
        password='',
        database=''
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM g7_plant_sensor_data WHERE inserted_timestamp = (SELECT MAX(inserted_timestamp) FROM g7_plant_sensor_data)")
    rows = cursor.fetchall()
    return rows


#print(get_soil_moisture_percentage())

while(True):
    push_sensor_data()
    print("Latest Data Pushed!")
    time.sleep(15)
    rows = fetch_latest_sensor_data()
    print("Latest Data Fetched!")
    print(rows)
    key, soil_moisture, temperature, humidity, timestamp_value = rows[0]
    if(soil_moisture < 5.0):
        trigger_water_pump()
    time.sleep(120)
    print("Repeating Cycle!")
