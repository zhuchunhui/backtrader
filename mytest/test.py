from datetime import datetime

dt = datetime.strptime('2021-01-29 09:00:00+00:00','%Y-%m-%d %H:%M:%S+00:00')
print(dt.date())