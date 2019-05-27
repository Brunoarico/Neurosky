import time
import bluetooth
import mindwavemobile.MindwaveDataPoints as dp
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
import textwrap
import csv
import os
import sys
import pygame
import colorsys
import numpy as np
from scipy import interpolate
import math

gap = 100
stroke = 7
radius = 1.6
sizex = 1366
sizey = 768

STAT_FILE = sys.argv[1]
ADDR = "74:E5:43:9C:60:32" #old neurosky
#ADDR = "C4:64:E3:E7:B9:E6" #new neurosky
x_len = 200
FPS = 60
xs = list(range(0, 200))

med_data = [0] * x_len
at_data = [0] * x_len

screen = pygame.display.set_mode((sizex, sizey))
clock = pygame.time.Clock()

def send2Pd (message=""):
    os.system("echo '" + message + "' | pdsend 3000")

def setTone (ch, val):
    message = str(ch)+ ' ' + str(val) + ';'
    print(message)
    send2Pd(message)



if __name__ == '__main__':
    dict = {'Meditation':'0', 'Attention':'0', 'delta':'0', 'theta':'0', 'lowAlpha':'0', 'highAlpha':'0', 'lowBeta':'0', "highBeta":'0', 'lowGamma':'0', 'midGamma':'0','PoorSignalLevel':'0'}
    f = open(STAT_FILE, "w")
    data_writer = csv.DictWriter(f, dict.keys(), delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writeheader()

    pygame.init()


    mindwaveDataPointReader = MindwaveDataPointReader(ADDR)
    mindwaveDataPointReader.start()

    if (mindwaveDataPointReader.isConnected()):
        med = []
        at = []

        running = True
        while(running):
            dict = {}

            attention = {}
            while(True):
                dataPoint = mindwaveDataPointReader.readNextDataPoint()
                if(dataPoint.__class__ is dp.PoorSignalLevelDataPoint):
                    poorSignalLevel =dataPoint.dict()
                    dict.update(poorSignalLevel)
                elif (dataPoint.__class__ is dp.AttentionDataPoint):
                    attention = dataPoint.dict()
                    setTone(0, attention.get('Attention'))
                    dict.update(attention)
                elif (dataPoint.__class__ is dp.MeditationDataPoint):
                    meditation = dataPoint.dict()
                    setTone(1, meditation.get('Meditation'))
                    dict.update(meditation)
                elif (dataPoint.__class__ is dp.EEGPowersDataPoint):
                     eegPowers = dataPoint.dict()
                     dict.update(eegPowers)
                if(('delta' in dict) and ('PoorSignalLevel' in dict) and ('Meditation' in dict) and ('Attention' in dict)):
                    print(dict)
                    data_writer.writerow(dict)
                    med_value = meditation.get('Meditation')
                    med.append(med_value)
                    med = med[-x_len:]

                    at_value = attention.get('Attention')
                    at.append(at_value)
                    at = at[-x_len:]
                    print(at)
                    #print(med)
                    change = med_value/100
                    screen.fill(pygame.color.Color(int(255 * (1-change)), int(0), int(255 * (change)),1))
                    poly = []
                    for i in range (0, len(at)-1):
                        deg = math.radians(i/(len(at))*360)
                        deg2 = math.radians((i+1)/(len(at))*360)
                        poly.append((1.5*at[i]*np.cos(deg)+sizex/2, 1.5*at[i]*np.sin(deg)+sizey/1.5))
                    if(len(poly) > 3):
                        pygame.draw.polygon(screen, pygame.color.Color("green"), poly)

                    if(len(med) > 3):
                        f = interpolate.interp1d(np.arange(len(med)), med, kind='cubic')
                        xnew = np.arange(0, len(med)-1, 0.1)
                        med_s = f(xnew)
                        for i in range (0, len(med_s)-1):
                            for k in range (0, sizey, gap):
                                pygame.draw.line(screen, pygame.color.Color("white"),(i*(sizex/len(med_s)), med_s[i]+k),((i+1)*(sizex/len(med_s)), med_s[i+1]+k) ,5)
                    else:
                        for i in range (0, len(med)-1):
                            for k in range (0, sizey, gap):
                                pygame.draw.line(screen, pygame.color.Color("white"),(i*(sizex/len(med)), med[i]+k),((i+1)*(sizex/len(med)), med[i+1]+k) ,5)

                        #pygame.draw.line(screen, pygame.color.Color("black"),(at[i]*np.cos(deg)+sizex/2, at[i]*np.sin(deg)+sizey/2),(at[i+1]*np.cos(deg2)+sizex/2, at[i+1]*np.sin(deg2)+sizey/2) ,5)
                        #print(at)

                    pygame.display.update()
                    clock.tick(FPS)
                    break

    else:
        print((textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", " ")))
