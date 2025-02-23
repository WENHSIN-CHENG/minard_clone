import sqlite3
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
## 連接資料庫
connection = sqlite3.connect('data/minard.db')
city_df = pd.read_sql("""SELECT * FROM cities;""",con=connection)
temp_df = pd.read_sql("""SELECT * FROM temperatures;""",con=connection)
troop_df = pd.read_sql("""SELECT * FROM troop;""",con=connection)
connection.close()
## 使用參數
loncs = city_df["lonc"].values
latcs = city_df["latc"].values
city_names = city_df["city"].values
rows = troop_df.shape[0]
lonps = troop_df["lonp"].values
latps = troop_df["latp"].values
survivals = troop_df["surviv"].values
direction = troop_df["direc"].values
temp_celsuis = (temp_df["temp"] * 5/4).astype(int)
lonts = temp_df["lont"].values
annotations = temp_celsuis.astype(str).str.cat(temp_df["date"],sep="°C ")
fig , axes = plt.subplots(nrows=2,figsize=(25,12),gridspec_kw={"height_ratios":[4,1]})
## 第０個軸物件
## 繪製地圖
m = Basemap(projection="lcc", resolution = "i", width = 1000000, height = 400000,lon_0 = 31, lat_0 = 55,ax=axes[0])
##設定起始位置和終點
m.drawcountries()
m.drawrivers()
m.drawparallels(range(54,58),labels=[True,False,False,False])
m.drawmeridians(range(23,56,2),labels=[False,False,False,True])
## 繪製城市圖
x , y = m(loncs,latcs)
for xi , yi , city_name in zip(x, y, city_names):
    axes[0].annotate(text=city_name,xy= (xi, yi),fontsize=14,zorder=2)
## 繪製軍隊圖
x , y = m(lonps , latps)
for i in range(rows -1):
    if direction[i] == "A":
        line_color = "tan"
    else:
        line_color = "black"
    start_stop_lons = (x[i],x[i + 1]) ## 兩點之間繪製
    start_stop_lats = (y[i],y[i + 1])
    line_width = survivals[i]
    m.plot(start_stop_lons,start_stop_lats,linewidth = line_width/10000, color= line_color,zorder=1)
## 第１個軸物件
## 繪製氣溫圖
axes[1].plot(lonts, temp_celsuis, linestyle="dashed",color="black")
for lons , temp_c, annotation in zip(lonts,temp_celsuis, annotations):
    axes[1].annotate(annotation, xy=(lons -0.3, temp_c - 7),fontsize=10)
axes[1].set_ylim(-50,10)
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
axes[1].spines["bottom"].set_visible(False)
axes[1].spines["left"].set_visible(False)
axes[1].grid(True,which="major",axis="both")
axes[1].set_xticklabels([])
axes[1].set_yticklabels([])
axes[0].set_title("Napolean's disastrous Russian campaign of 1812", loc="left",fontsize=30)
plt.tight_layout()
fig.savefig("minard_clone.png")
