import time
import bluetooth
import mindwavemobile.MindwaveDataPoints as dp
from mindwavemobile.MindwaveDataPointReader import MindwaveDataPointReader
import textwrap
import csv
import os
import sys

STAT_FILE = sys.argv[1]
#ADDR = "74:E5:43:9C:60:32"
ADDR = "C4:64:E3:E7:B9:E6"

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

    mindwaveDataPointReader = MindwaveDataPointReader(ADDR)
    mindwaveDataPointReader.start()

    if (mindwaveDataPointReader.isConnected()):
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
                dict = {}
    else:
        print((textwrap.dedent("""\
            Exiting because the program could not connect
            to the Mindwave Mobile device.""").replace("\n", " ")))
