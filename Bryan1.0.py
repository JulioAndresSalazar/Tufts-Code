#!/usr/bin/python3
ev3 = Device("this")
def manageRange(n):
	return max(min(n,1050),-1050)
def main():
	#2 = Blue
	#3 = Green
	#5 = Red
	sensor_1 = None
	sensor_2 = None
	sensor_3 = None
	sensor_4 = None
	occurrence_array = []
	one_array = [1, 1, 2]
	two_array = [0, 2, 2]
	three_array = [0, 1, 3]
	four_array = [0, 0, 4]
	sensor_array = [0, 0, 0, 0]
	motorB = ev3.LargeMotor('outD')
	motorC = ev3.LargeMotor('outC')
#read each sensor and store in first array
	sensor_1 = ev3.ColorSensor('in1').color
	print(sensor_1)
	sensor_array[0] = sensor_1
	sensor_2 = ev3.ColorSensor('in2').color
	print(sensor_2)
	sensor_array[1] = sensor_2
	sensor_3 = ev3.ColorSensor('in3').color
	print(sensor_3)
	sensor_array[2] = sensor_3
	sensor_4 = ev3.ColorSensor('in4').color
	print(sensor_4)
	sensor_array[3] = sensor_4
	print(sensor_array)
	occurrence_array.append(sensor_array.count(5))
	occurrence_array.append(sensor_array.count(3))
	occurrence_array.append(sensor_array.count(2))
	print(occurrence_array)
	occurrence_array.sort()
	print(occurrence_array)
	if occurrence_array == one_array:
		motorB.run_forever(speed_sp = 500,stop_action="brake")
		motorC.run_forever(speed_sp = 500,stop_action="brake")
		sleep(3)
	if occurrence_array == two_array:
		motorB.run_forever(speed_sp = 400,stop_action="brake")
		motorC.run_forever(speed_sp = 400,stop_action="brake")
		sleep (2)
	elif occurrence_array == three_array:
		motorB.run_forever(speed_sp = 300,stop_action="brake")
		motorC.run_forever(speed_sp = 300,stop_action="brake")
		sleep(2)
	elif occurrence_array == four_array:
		motorB.run_forever(speed_sp = 200,stop_action="brake")
		motorC.run_forever(speed_sp = 200,stop_action="brake")
		sleep(1)
if __name__ == '__main__':
	main()


