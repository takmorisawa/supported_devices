import pandas as pd
import os
import re

def postprocess():

    current_dir=os.path.dirname(os.path.abspath(__file__))
    print("processing...{0}".format(current_dir))

    df_maker=pd.read_csv(os.path.join(current_dir,"current/csv/devices_ymobile-maker-scraped.csv"),index_col=1)

    df=pd.read_csv(os.path.join(current_dir,"current/csv/devices_ymobile-scraped.csv"),index_col=0,dtype=str)
    df_edited=pd.DataFrame()

    for idx,col in df.iterrows():

        # maker
        m=re.match("section-(.+?) .+",col["maker"])
        col["maker"]=m.groups()[0].strip() if m else col["maker"]
        key="cat-"+col["maker"]
        col["maker"]=df_maker.loc[key]["name"] if key in df_maker.index else ""

        # モデルにマッチ（
        m=re.match("(.+)（(.+)）",col["name"])
        col["name"]=m.groups()[0].strip() if m else col["name"]
        col["model"]=m.groups()[1].strip() if m else ""

        # simの分割
        m=re.match("(.+)/(.+)",col["sim"] if type(col["sim"]) is str else "")
        col["sim1"]=m.groups()[0].strip() if m else col["sim"]
        col["sim2"]=m.groups()[1].strip() if m else ""
        col=col.drop("sim")

        # 不要な注記を除去
        col["name"]=col["name"].replace("™","")
        col["name"]=col["name"].replace("®","")
        col["os"]=(col["os"] if type(col["os"]) is str else "").replace("™","")

        # function
        dict={"音声通話":"call","SMS":"sms","データ通信":"data","テザリング":"tethering"}
        for kv in re.findall("'(.+?)：(.*?)'",col["func"]):
            col[dict[kv[0]]]=kv[1]

        # carrierを分割
        for carrier in [item for item in re.findall("'.+?'",col["carrier"]) if item!="'undefined'"]:
            col=col.copy()
            col["carrier"]=carrier.strip("\'")
            df_edited=df_edited.append(col,ignore_index=True)

    # カラムの並び替え
    #df_edited=df_edited.loc[:,["device_type","maker","name","model","carrier","unlock","org_name","sim","os","note"]]

    df_edited.index.name="id"
    df_edited.to_csv(os.path.join(current_dir,"current/csv/devices_ymobile-scraped-edited.csv"))


if __name__ == '__main__':

    postprocess()
