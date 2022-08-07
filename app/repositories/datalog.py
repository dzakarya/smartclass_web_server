

def get_current_data(date : str, time : str ):
    if len(date) != 10 :
        split_date = date.split("-")
        for i in range(len(split_date)):
            if len(split_date[i]) != 2:
                split_date[i] = "0"+split_date[i]
                print(split_date[i])
