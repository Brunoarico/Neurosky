import pandas as pd
import matplotlib.pyplot as plt
import sys

if(sys.argv[1] == "-h"):
    print("use command  ./python3 ploter <filename> [option] \n \
    options:\n\
          -1    Meditation\n\
          -2    Attention\n\
          -3    delta\n\
          -4    theta\n\
          -5    lowAlpha\n\
          -6    highAlpha\n\
          -7    lowBeta\n\
          -8    highBeta\n\
          -9    lowGamma\n\
          -10   midGamma\n\
          -allStats\n\
          -allWaves\
          ")
else:
    try:
        df = pd.read_csv(sys.argv[1]+".log", delimiter=",")
        opt = sys.argv[2]
        ok = False
        if(opt == "-1"  or opt == "-allStats"):
            plt.plot(df['Meditation'], 'r-', label="Meditation")
            ok = True
        if(opt == "-2" or opt == "-allStats"):
            plt.plot(df['Attention'], 'b-', label="Attention")
            ok = True
        if(opt == "-3" or opt == "-allWaves"):
            plt.plot(df['delta'], 'r-', label="Delta")
            ok = True
        if(opt == "-4" or opt == "-allWaves"):
            plt.plot(df['theta'], 'g-', label="Theta")
            ok = True
        if(opt == "-5" or opt == "-allWaves"):
            plt.plot(df['lowAlpha'], 'b-', label="Low Alpha")
            ok = True
        if(opt == "-6" or opt == "-allWaves"):
            plt.plot(df['highAlpha'], 'c-', label="High Alpha")
            ok = True
        if(opt == "-7" or opt == "-allWaves"):
            plt.plot(df['lowBeta'], 'm-', label="Low Beta")
            ok = True
        if(opt == "-8" or opt == "-allWaves"):
            plt.plot(df['highBeta'], 'y-', label="High Beta")
            ok = True
        if(opt == "-9" or opt == "-allWaves"):
            plt.plot(df['lowGamma'], 'k-', label="Low Gamma")
            ok = True
        if(opt == "-10" or opt == "-allWaves"):
            plt.plot(df['midGamma'], color = "#11ff55", label="Mid Gamma")
            ok = True
        if(not ok):
            print("Invalid Option!")
            sys.exit()

        plt.legend()
        plt.show()

    except:
        print("Invalid file name")
