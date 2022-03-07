import datetime


async def df():
    date_time = datetime.datetime.now()
    new_time = datetime.timedelta(hours=5)
    final_time = new_time + date_time
    final_time = final_time.strftime("%Y-%m-%d %H:%M")
    return final_time