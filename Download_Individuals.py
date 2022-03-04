import pandas as pd
import getNetLoad as gnet
import time
from datetime import  datetime

direct_path = r'C:\Users\sealc\PycharmProjects\LandingPage\Data\NetData'
iteration = 0
while True:
    iteration+=1
    print(datetime.now())
    # do work
    wind = gnet.getwind()
    wind.to_csv(direct_path + '\\' + 'wind.csv', index=False)

    solar = gnet.getsolar()
    solar.to_csv(direct_path +  '\\' + 'solar.csv', index=False)

    outage = gnet.getoutage()
    outage.to_csv(direct_path +  '\\' + 'outage.csv', index=False)

    sevenDay = gnet.get7daydemand()
    sevenDay.to_csv(direct_path + '\\' + 'sevenDay.csv', index=False)

    print('success')
    time.sleep(300 * 5)