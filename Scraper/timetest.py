from datetime import datetime, timedelta
import time
if __name__ == '__main__':
    cur_time = datetime.now()+timedelta(1)
    print(cur_time)
    today_date = datetime.today()
    print(today_date)
    today_time = today_date + timedelta(hours = 20, minutes = 30)
    my_date = datetime(today_date.year, today_date.month, (today_date.day+1))
    #final_time = today_date.combine(today_date, today_time)
    print(my_date)
    print(today_time)
    time.sleep(15)