

def get_current_data(date : str, time : str ):
    if len(date) != 10 :
        split_date = date.split("-")
        for i in range(len(split_date)):
            if len(split_date[i]) < 2:
                split_date[i] = "0"+split_date[i]
            if i < len(split_date)-1:
                split_date[i] = split_date[i]+"-"
        date="".join(map(str,split_date))
    print(date)
    if len(time) != 5 :
        split_time = time.split("-")
        for i in range(len(split_time)):
            if len(split_time[i]) < 2:
                split_time[i] = "0"+split_time[i]
            if i < len(split_time)-1:
                split_time[i] = split_time[i]+":"
        time="".join(map(str,split_time))
    print(time)
        