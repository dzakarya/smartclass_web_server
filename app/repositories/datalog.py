from ..model.data_handler import DataHandler
from ..schemas.api_response import GetDataLog
from loguru import logger

def get_current_data(date : str, time : str )->GetDataLog:
    if len(date) != 10 :
        split_date = date.split("-")
        for i in range(len(split_date)):
            if len(split_date[i]) < 2:
                split_date[i] = "0"+split_date[i]
            if i < len(split_date)-1:
                split_date[i] = split_date[i]+"-"
        date="".join(map(str,split_date))

    if len(time) != 5 :
        split_time = time.split(":")
        for i in range(len(split_time)):
            if len(split_time[i]) < 2:
                split_time[i] = "0"+split_time[i]
            if i < len(split_time)-1:
                split_time[i] = split_time[i]+":"
        time="".join(map(str,split_time))
    
    DlHandler = DataHandler()
    result = GetDataLog(
        temperature=0,
        smoke=0,
        light=0,
        people=0
    )

    try:
        result.temperature = DlHandler.get_temp_value(date, time)
    except Exception as e:
        logger.error(e)
        result.temperature = 0

    try:
        result.smoke = DlHandler.get_smoke_value(date, time)
    except Exception as e:
        result.smoke = 0
        logger.error(e)

    try:
        result.light = DlHandler.get_light_value(date, time)
    except Exception as e:
        result.light = 0
        logger.error(e)
    return result