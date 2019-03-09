import requests
import json
import time
import RPi.GPIO as GPIO

# Sets pin configuration (DO NOT CHANGE)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN) #WHITE
GPIO.setup(23, GPIO.IN) #RED
GPIO.setup(12, GPIO.IN) #BLUE
GPIO.setup(21, GPIO.IN) #YELLOW
        
#Define functions 
def attempt(position, Color1, Color2, Color3, Color4):
    print ("Hold down " + str(position) + ' color') 
    time.sleep(4) 
    if GPIO.input(Color1) == 1:
        #if correct, move to next color i.e. pass 
        pass
    elif GPIO.input(Color2) or GPIO.input(Color3) or GPIO.input(Color4) == 1:
        print("Incorrect, resetting...")
        attempt('FIRST', Color1, Color2, Color3, Color4)
        time.sleep(2)
    else: 
        print('No color recevied, resetting...')
        time.sleep(2)
        attempt('FIRST', Color1, Color2, Color3, Color4)
        pass 
    
def finalattempt(position, Color1, Color2, Color3, Color4):
    print ("Hold down " + str(position) + ' color') 
    time.sleep(4) 
    if GPIO.input(Color1) == 1:
        #if correct, move to next color i.e. pass 
        print('SOLVED!!!!')
        updatetag()
    elif GPIO.input(Color2) or GPIO.input(Color3) or GPIO.input(Color4)== 1:
        print("Incorrect, resetting...")
        attempt('FIRST', Color1, Color2, Color3, Color4)
        time.sleep(2)
    else: 
        print('No color recevied, resetting...')
        time.sleep(2)
        attempt('FIRST', Color1, Color2, Color3, Color4)
        pass 
    #CURRENT SOLUTION: Yellow, Orange, Red, Blue
def updatetag():
    #Enter tag name and type i.e. "height" and "DOUBLE"
    Tag = "LEDPuzzleConfirmation"
    Type = "STRING"
    #Do not change:
    Value = "SOLVED"
    urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
    urlTag = urlBase + Tag
    urlValue = urlBase + Tag + "/values/current"
    headers = {"Content-Type":"application/json","Accept":"application/json","x-ni-api-key":"sfIbD4eYzaMBqna_rZW5XQL2BR77CLb2I4BDvI6uxt"}
    propName={"type":Type,"path":Tag}
    propValue = {"value":{"type":Type,"value":Value}}
    requests.put(urlValue,headers=headers,json=propValue).text 

#Color-Pin designations 
#14 = WHITE
#23 = RED
#12 = BLUE
#21 = YELLOW

#Decide what code is here:
Color1 = 23
Color2 = 12
Color3 = 21
Color4 = 14

#RBYW

#timing is tricky with first users 
#Chris held down all colors
#migrate to huzzah 

attempt('FIRST', Color1, Color2, Color3, Color4)
attempt('SECOND', Color2, Color1, Color3, Color4)
attempt('THIRD', Color3, Color1, Color2, Color4)
finalattempt('FOURTH', Color4, Color1, Color2, Color3)
