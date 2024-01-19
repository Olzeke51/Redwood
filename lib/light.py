# Grove light sensor v1.2

# from machine import ADC
# from time import sleep

light = ADC(0)
lightVal = light.read_u16()
print('lightvalue= ')
print(str(lightVal))
sleep(1)

    

