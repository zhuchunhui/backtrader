from datetime import datetime
import time
from datetime import date

# dt = datetime.strptime('2021-01-29 09:00:00+00:00','%Y-%m-%d %H:%M:%S+00:00')
# print(dt.date())
# print(time.time())

timeArray = time.localtime(int(1617640758))
print(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))

# stamp=time.mktime(time.strptime('2016-11-24 14:00:21', '%Y-%m-%d %H:%M:%S'))
# print(int(stamp))
