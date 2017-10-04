#!/usr/bin/env python
import RPi.GPIO as GPIO
from time import sleep
import os
import subprocess

# Setup getting an image
def get_video(state):
  folderName = "/home/pi/HumphreyData/"
	if os.path.isdir(folderName)== False:
	  os.makedirs(folderName)
    fileNumber = 1
    filePath = folderName + str(fileNumber) + ".h264"
    while os.path.isfile(filePath):
      fileNumber += 1
      filePath = folderName + str(fileNumber) + ".h264"

    fileName = str(fileNumber)
	cmdStr = "sudo raspivid -n -w 1024 -h 768 -t 0 -fps 2 -o %s/%s.h264" %(folderName, fileName)
  if state:
    capture = subprocess.Popen(cmdStr, shell=True)
  else:
    pid = "sudo pkill -15 -f raspivid"
    os.system(pid)

# Setup LED control
def switch_LED(state):
	for item in LEDpins:
    GPIO.output(item, state)

# Setup GPIO config
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Setup GPIO pins
LEDpins  = [19, 21]
switchState = 23

# If true, LEDS are off -> GPIO pins are current sinks
lOn  = False
lOff = True

# Configure LED GPIO pins
for item in LEDpins:
  GPIO.setup(item, GPIO.OUT)
	GPIO.output(item, lOff)

# Configure switch GPIO pins
GPIO.setup(switchState, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Scipt ready flash
flashes = 1
while flashes < 4:
  switch_LED(lOn)
	sleep(0.5)
	switch_LED(lOff)
	sleep(0.5)
	flashes += 1

# Pin check loop
while True:
  if GPIO.input(switchState):
    captureState = False
    switch_LED(lOff)
  else:
    captureState = True
    switch_LED(lOn)

  get_video(captureState)
  GPIO.wait_for_edge(switchState, GPIO.BOTH)
  sleep(0.2)

# Script cleanup
GPIO.cleanup()
