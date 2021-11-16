import os
import time
from datetime import datetime

import psutil

device_id = os.getenv("DEVICE_ID")

stats_dir = "/export/stats/" + device_id

os.makedirs(stats_dir)

while True:
    file_name = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
    f = open(stats_dir + "/" + file_name, "w")

    memory_usage = psutil.virtual_memory()[2]
    f.write("MEM=%a\n" % memory_usage)

    f.close()
    time.sleep(15)
