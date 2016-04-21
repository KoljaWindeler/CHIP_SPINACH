from time import localtime,  sleep 
import arduino_bridge
import json
import urllib.request

zero = [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]]
one = [[0,1,0],[0,1,0],[0,1,0],[0,1,0],[0,1,0]]
two = [[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]]
three = [[1,1,1],[0,0,1],[1,1,1],[0,0,1],[1,1,1]]
four = [[1,0,0],[1,0,1],[1,1,1],[0,0,1],[0,0,1]]
five = [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]]
six = [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]]
seven = [[1,1,1],[0,0,1],[0,0,1],[0,0,1],[0,0,1]]
eight = [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]]
nine = [[1,1,1],[1,0,1],[1,1,1],[0,0,1],[1,1,1]]

display = [zero,one,two,three,four,five,six,seven,eight,nine]

# prepare vars
pin = 6
LC = 38	# spinach dip has 38 leds
with_date = 1
with_temp = 0
offset = 4
dimm_value = 60 # divide by 15
on_value = 60
temp_timeout = 60*60 # 1x per hour

# setup salsa
#salsa = arduino_bridge.connection()
#salsa.setup_ws2812_unique_color_output(pin,LC)

colorArray = [arduino_bridge.Color(0,0,0) for i in range(LC)]
black = arduino_bridge.Color(0, 0, 0) # off
debugArray = bytearray(38)
check_age = temp_timeout

while 1:
	# get temp
	if(check_age>=temp_timeout):
		j = json.loads(urllib.request.urlopen('http://api.wunderground.com/api/917b4dab82461e13/geolookup/conditions/forecast/q/Germany/Langenhagen.json').read().decode("utf-8"))
		print("now: "+str(j['current_observation']['temp_c']))
		print("max: "+str(j['forecast']['simpleforecast']['forecastday'][0]['high']['celsius']))
		print("min: "+str(j['forecast']['simpleforecast']['forecastday'][0]['low']['celsius']))
		display_this = j['current_observation']['temp_c'])
		check_age = 0
	check_age += 1

	# switch all of
	for i in range(LC):
		colorArray[i].copy(black)
		debugArray[i]=0
		
	# generate color, shall be dynamic later therefor in loop
	first_digit_color = arduino_bridge.Color(on_value, 0, 0) # red
	second_digit_color = arduino_bridge.Color(0, 0, on_value) # blue
	
	first_digit = display_this//10
	second_digit = display_this%10
	
	for x in range(0,3):
		for y in range(0,5):
			if(display[first_digit][y][x]):
				colorArray[offset+x+6*y].copy(first_digit_color)
				debugArray[offset+x+6*y]=1
			if(display[second_digit][y][x]):
				colorArray[offset+x+6*y+3].copy(second_digit_color)
				debugArray[offset+x+6*y+3]=1
	
	i=0
	print(display_this)
	for y in range(0,7):
		for x in range(0,6):
			if(x==0):
				print("")
			if(y==0 or y==6):
				if(x==0 or x==5):
					print("x",end="")
				else:
					print(debugArray[i],end="")
					i+=1
			else:
				print(debugArray[i],end="")
				i+=1
	print("")
	# send it to the salsa driver
	#salsa.ws2812set(pin,colorArray)
	sleep(1)
