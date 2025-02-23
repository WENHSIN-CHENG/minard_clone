import pandas as pd 
import sqlite3 

class CreateMinardDB:
    def __init__(self):
        with open("data/minard.txt") as f:
            lines = f.readlines()
##定義欄位名稱
        column_names = lines[2].split()                             
        patterns_to_be_replace = {"(",")","$",","}
        adjust_column_name = []
        for column_name in column_names:
            for patten in patterns_to_be_replace:
                if patten in column_name:
                    column_name = column_name.replace(patten , "")
            adjust_column_name.append(column_name)
        self.lines = lines
        self.column_names_city = adjust_column_name[:3]
        self.column_names_temp = adjust_column_name[3:7]
        self.column_names_troop = adjust_column_name[7:]
##載入城市資料
    def create_city_dataframe(self):
        i = 6
        longitudes , latitudes , cities = [] , [], []
        while i <= 25:
            long , lat , city = self.lines[i].split()[:3]
            longitudes.append(float(long))
            latitudes.append(float(lat))
            cities.append(city)
            i += 1
        city_data = (longitudes,latitudes,cities)
        city_df = pd.DataFrame()
        for column_name, data in zip(self.column_names_city,city_data):
            city_df[column_name] = data
        return city_df
##載入氣溫資料
    def create_temperature_dataframe(self):
        i = 6
        longitudes , temperatures , days , dates = [],[],[],[]
        while i <= 14:
            lines_split = self.lines[i].split()
            longitudes.append(float(lines_split[3]))
            temperatures.append(float(lines_split[4]))
            days.append(int(lines_split[5]))
            if i == 10:
                dates.append("Nov 24")
            else:
                date_str = lines_split[6] + " " + lines_split[7]
                dates.append(date_str)
            i += 1
        temperature_data = (longitudes,temperatures,days,dates)
        temperature_df = pd.DataFrame()
        for column_name , data in zip(self.column_names_temp,temperature_data):
            temperature_df[column_name] = data
        return temperature_df
## 載入軍隊資料
    def create_troop_dataframe(self):
        i = 6 
        longitudes, latitudes , survivals, directions, divisions = [],[],[],[],[]
        while i <= 53:
            lines_split = self.lines[i].split()
            divisions.append(int(lines_split[-1]))
            directions.append(lines_split[-2])
            survivals.append(int(lines_split[-3]))
            latitudes.append(float(lines_split[-4]))
            longitudes.append(float(lines_split[-5]))
            i += 1
        troop_data = (longitudes,latitudes,survivals,directions,divisions)
        troop_df = pd.DataFrame()
        for column_name , data in zip(self.column_names_troop,troop_data):
            troop_df[column_name] = data
        return troop_df
## 建立資料庫
    def create_database(self):
        connection = sqlite3.connect("data/minard.db")
        city_df = self.create_city_dataframe()
        temperature_df = self.create_temperature_dataframe()
        troop_df = self.create_troop_dataframe()
        df_dict = {
            "cities" : city_df,
            "temperatures" : temperature_df,
            "troop" : troop_df
        }
        for k , v in df_dict.items():
            v.to_sql(name=k , con=connection, index = False , if_exists= "replace")


create_minard_db = CreateMinardDB()
create_minard_db.create_database()