#Import required libraries
import time, math, operator, PIL, random
import numpy as np
from PIL import Image, ImageDraw, ImageChops
from functools import reduce

#Algorithm Setup
map_file = "MarioMap.png" #choose image file here
map = Image.open(map_file) #resets map file
range = map.size 
box_1 = range[0]*0.05 
box_2 = range[1]*0.1 
draw = ImageDraw.Draw(map)
maxDiff = 100000 

def make_box(coordinates):
    #This function crops a picture around a given set of coordinates 
    refX = coordinates[0]
    refY = coordinates[1]
    refLeft = refX - (box_1) 
    refTop = refY - (box_1) 
    refRight = refLeft + (box_2) 
    refBottom = refTop + (box_2) 
    refBox = (refLeft, refTop, refRight, refBottom)
    refMap = map.crop(refBox)
    return(refMap)

def originalScatter(numParticles, map,box_1):
    #This function randomly distributes a number of particles across the image map
    draw = ImageDraw.Draw(map)
    i=0
    particleArray = []
    print('Drawing particles on map...')
    time.sleep(2)
    while i < numParticles:
        x = np.random.uniform(box_1,range[0]-box_1)
        y = np.random.uniform(box_1, range[1]-box_1)
        weight = 1
        scaling = 30 
        draw.ellipse(((x,y),((x+weight*scaling),(y+scaling*weight))), fill = 'Red', outline = 'Red')
        particleArray.append([x,y,weight])
        i = i+1
    #print(particleArray) #Prints particle array. NOT Recommended
    return(map, particleArray)

def draw_rectangle(coordinates):
    #This function draws a rectangle on the map wherever the observer is 
    map = Image.open(map_file)
    draw = ImageDraw.Draw(map)
    left = coordinates[0] - box_1
    top = coordinates[1] - box_1
    right = left + box_2
    bottom = top + box_2
    draw.rectangle(((left, top), (right, bottom)), fill=None, outline = 'Blue', width = 20)
    return map

def find_origin():
    #This function finds an origin to place observer initially
    x_0 = np.random.uniform(box_1,range[0]-box_1)
    y_0 = np.random.uniform(box_1,range[1]-box_1)
    origin = (x_0, y_0)
    print('Origin: ' + str(origin))
    return origin

def weightUpdate(particleArray,coordinates):
    #This function changes the weights of particles based on how likely observer is located there
    print('Updating weights and resampling, please wait...')
    left = coordinates[0] - box_1
    top = coordinates[1] - box_1
    right = left + box_2
    bottom = top + box_2
    obsBox = (left, top, right, bottom)
    obsMap = map.crop(obsBox)
    for i in particleArray:
        refCoords = (i[0], i[1])
        refMap=make_box(refCoords) 
        #refMap.show() #Shows image at each particle. NOT Recommended
        imageDiff = compare(refMap,obsMap) #lower image difference  = better match
        #print('imageDiff: ' , imageDiff) #OPTIONAL
        scaling = 18750 
        i[2] = scaling/(imageDiff/maxDiff) 
    return particleArray

def compare(refMap, obsMap):
    #This function compares two images and returns a value
    if refMap.size != obsMap.size or refMap.getbands() != obsMap.getbands():
        print("no go")
        return -1
    imgDiff = 0
    for band_index, band in enumerate((refMap).getbands()):
        m1 = np.array([p[band_index] for p in refMap.getdata()]).reshape(*refMap.size)
        m2 = np.array([p[band_index] for p in obsMap.getdata()]).reshape(*obsMap.size)
        imgDiff += np.sum(np.abs(m1-m2))
    return(imgDiff)

def drawParticles(updated_array, map):
    #This function draws particles on the map given their coordinate array
    draw = ImageDraw.Draw(map)
    for particle in updated_array:
        x = particle[0] #x-coordinate
        y = particle[1] #y-coordinate
        weight = particle[2] #weight
        draw.ellipse(((x,y),((x+(weight)),(y+(weight)))), fill = 'Red', outline = 'Red')
    return(map)
        #print(particleArray) #OPTIONAL: prints the array

def observerMovement(coordinates):
    #This function produces a random movement vector with some noise for observer
    while True:
        dx = np.random.uniform(-100,100)    
        dy_list = [math.sqrt(10000-dx**2), -math.sqrt(10000-dx**2)]
        dy = random.choice(dy_list)
        dx_noise = np.random.uniform(-40,40) #Adjust depending on how much noise we want
        dy_noise = np.random.uniform(-40,40)
        x = coordinates[0] + dx + dx_noise
        y = coordinates[1] + dy + dy_noise
        movement_vector = (x,y)
        if movement_vector[0] < box_1 or movement_vector[0] > range[0] - box_1 or movement_vector[1] < box_1 or movement_vector[1] > range[1] - box_1:
            pass    
        else:
            return(x,y,dx,dy)

def particleMovement(particleArray, movement_vector):
    #This function defines how the particles move 
    for particle in particleArray:
        dx = movement_vector[2]
        dy = movement_vector[3]
        dx_noise = np.random.uniform(-40,40) #Adjust depending on how much noise we want
        dy_noise = np.random.uniform(-40,40) 
        particle[0] = particle[0] + dx + dx_noise
        particle[1] = particle[1] + dy + dy_noise
    return(particleArray)

def showMap(map, coordinates, weighted_array):
    #Displays the image given the particle array and observer coordinates
    map = Image.open(map_file) 
    rectangle_map = draw_rectangle(coordinates) 
    updated_Map = drawParticles(weighted_array, rectangle_map)
    updated_Map.resize((650,650)).show()
    print('Map updated...')


def resample(weighted_array): 
    #Determines if a particle is large or small and then moves small particles to larger particles, then resets their weight
    weight_list =[]
    for particle in weighted_array:
        weight = particle[2]
        weight_list.append(weight)
    criteria = 1.05*(sum(weight_list)/len(weight_list)) 
    large_particles = [] 
    small_particles = []
    for particle in weighted_array: 
        weight = particle[2] 
        if weight < criteria: 
            particle[2] = 30     
            small_particles.append([particle[0], particle[1], particle[2]])
        else:
            particle[2] = 30 
            large_particles.append([particle[0], particle[1], particle[2]])
    weighted_array = large_particles
    for particle in small_particles:
        refParticle = random.choice(large_particles)
        particle[0] = refParticle[0] 
        particle[1] = refParticle[1] 
        weighted_array.append(particle)
    return weighted_array 

def lastLoop(map, origin, box_1, resampled_array):
    #This function moves observer, moves the particles, then goes through resampling loop
    map = Image.open(map_file)
    print('Getting movement vector, please wait...')
    movement_vector = observerMovement(origin)
    moved_array = particleMovement(resampled_array, movement_vector) 
    showMap(map, movement_vector, moved_array) 
    origin = movement_vector
    return (movement_vector, moved_array)
        
numParticles = range[0]/10 #one particle for every 10 pixels, can be adjusted

#INITIAL STEP#
origin = find_origin() #finds origin
refMap = make_box(origin) #stores origin pic as refMap
#refMap.show(command=open) #optional showing of origin pic
rectangle_map = draw_rectangle(origin) #redraws origin rectangle on the map
particle_data = originalScatter(numParticles, rectangle_map, box_1)#get particle data
drawn_map = particle_data[0] #this map has both rectangle and particles
particle_Array = particle_data[1] #this is particle array
print('Displaying map')
drawn_map.resize((650,650)).show() #shows the drawn on map
time.sleep(2)
#END OF INITIAL STEP#

#START OF PARTICLE FILTER ALGORITHM
time_steps = 8 #choose the amount of time steps to run for
i = 0
while i < time_steps:
    weighted_array = (weightUpdate(particle_Array, origin)) 
    #NOTE: takes a bit to compute
    #showMap(map, origin, weighted_array) #show new weights #OPTIONAL
    resampled_array = resample(weighted_array) 
    final_data = lastLoop(map, origin, box_1, resampled_array)
    origin = final_data[0]
    particle_Array = final_data[1]
    i = i + 1
#END OF ALGORITHM
    
