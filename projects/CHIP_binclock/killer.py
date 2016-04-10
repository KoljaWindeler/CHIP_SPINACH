from time import localtime,  sleep 
import arduino_bridge

# prepare bin arrays
t_max_bin=bytearray(6)
t_min_bin=bytearray(6)
month_bin=bytearray(6)
day_bin=bytearray(6)
hour_bin=bytearray(6)
min_bin=bytearray(6)
sec_bin=bytearray(6)

# prepare vars
pin = 6
LC = 38	# spinach dip has 38 leds
with_date = 0
with_temp = 0
offset = 0
dimm_value = 15
if(with_temp and with_date):
	exit("only date OR temperature")

# setup salsa
salsa = arduino_bridge.connection()
salsa.setup_ws2812_unique_color_output(pin,LC)

colorArray = [arduino_bridge.Color(0,0,0) for i in range(LC)]

while 1:
	# generate color, shall be dynamic later therefor in loop
	temp_max_color = arduino_bridge.Color(0, 0, 0) # red
	temp_min_color = arduino_bridge.Color(0, 0, 0) # blue
	month_color = arduino_bridge.Color(0, 0, 0)	 # red
	day_color = arduino_bridge.Color(0, 0, 0)	 # cyan
	hour_color = arduino_bridge.Color(0, 0, 0)	 # blue
	min_color = arduino_bridge.Color(0, 0, 0)	 # yellow
	sec_color = arduino_bridge.Color(0, 0, 0)	 # green	

	# generate bin array for time, date and temp
	for i in range(0,6):
		t_max_bin[5-i] = int((22  // 2**i) % 2)	# todo, get local temp, remember, only 6 leds so 63 is max, i reccommend Celsius :)
		t_min_bin[5-i] = int((8 //  2**i) % 2)	# todo, get local temp, remember, only 6 leds so 63 is max, i reccommend Celsius :)
		
		month_bin[5-i] = int((localtime().tm_mon  // 2**i) % 2)
		day_bin[5-i]   = int((localtime().tm_mday // 2**i) % 2)
		hour_bin[5-i]  = int((localtime().tm_hour // 2**i) % 2)
		min_bin[5-i]   = int((localtime().tm_min  // 2**i) % 2)
		sec_bin[5-i]   = int((localtime().tm_sec  // 2**i) % 2)

	# print for debug
	if(with_date):
		print(str(localtime().tm_mon)+"."+str(localtime().tm_mday)+". "+str(localtime().tm_hour)+":"+str(localtime().tm_min)+":"+str(localtime().tm_sec))
		print(month_bin)
		print(day_bin)
	else:
		print(str(localtime().tm_hour)+":"+str(localtime().tm_min)+":"+str(localtime().tm_sec))
	print(hour_bin)
	print(min_bin)
	print(sec_bin)
	print()

	# copy bin time to color array
	for i in range(0,6):
		if(with_date):
			colorArray[offset+i+6*0] = month_color				# 04-09, with offset = 4
			colorArray[offset+i+6*1] = day_color				# 04-09, with offset = 4
			if(not(month_bin[i])):
				colorArray[offset+i+6*0].dimm(5)			# 04-09, with offset = 4
			if(day_bin[i]):
				colorArray[offset+i+6*1].dimm(5)			# 10-15

		if(with_temp):
			colorArray[offset+i+6*0] = temp_max_color			# 04-09, with offset = 4
			colorArray[offset+i+6*1] = temp_min_color			# 04-09, with offset = 4
			if(t_max_bin[i]):
				colorArray[offset+i+6*0].dimm(dimm_value)		# 04-09
			if(t_min_bin[i]):
				colorArray[offset+i+6*1].dimm(dimm_value)		# 10-15


		colorArray[offset+i+6*(0+2*(with_date+with_temp))].copy(day_color)	# 04-09, 16-21
		colorArray[offset+i+6*(1+2*(with_date+with_temp))].copy(min_color)	# 10-15, 22-27
		colorArray[offset+i+6*(2+2*(with_date+with_temp))].copy(sec_color)	# 16-21, 28-33

		if(not(hour_bin[i])):
			colorArray[offset+i+6*(0+2*(with_date+with_temp))].dimm(dimm_value)

		if(not(min_bin[i])):
			colorArray[offset+i+6*(1+2*(with_date+with_temp))].dimm(dimm_value)

		if(not(sec_bin[i])):
			colorArray[offset+i+6*(2+2*(with_date+with_temp))].dimm(dimm_value)
	

	# send it to the salsa driver
	salsa.ws2812set(pin,colorArray)
	sleep(1)
