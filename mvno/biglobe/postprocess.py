import pandas as pd
import os
import re

def postprocess():

    current_dir=os.path.dirname(os.path.abspath(__file__))
    print("processing...{0}".format(current_dir))

    df=pd.read_csv(os.path.join(current_dir,"current/csv/devices_biglobe-scraped.csv"),index_col=0)
    df_edited=pd.DataFrame()
    dfA_edited=pd.DataFrame()


    # 対象をスマートフォンに限る（必要あり？）
    for idx,col in df.iterrows():

        col["org_name"]=col["name"]

        # name
        m=re.match("([^/]+)/([^/]+)",col["name"]) # モデル名称にマッチ
        col["name"]=m.groups()[1].strip() if m else col["name"]
        col["maker"]=m.groups()[0].strip() if m else col["name"]
        model=m.groups()[1].strip() if m else ""

        # carrier, model
        m=re.match("(.+)\((.+販売)版：(.+)\)$",col["name"])
        if m:
            col["name"]=m.groups()[0] if m else ""
            col["carrier"]=m.groups()[1] if m else ""
            col["model"]=m.groups()[2] if m else ""
        else:
            # model
            m=re.match("(.+)\((.+)\)$",col["name"])
            col["name"]=m.groups()[0] if m else col["name"]
            col["model"]=m.groups()[1] if m else ""

        # carrier
        m=re.match("([^/]+)/([^/]+)",col["device_type"])
        col["device_type"]=m.groups()[0].strip() if m else col["device_type"]
        col["os"]=m.groups()[1].strip() if m else col["os"]

        col["call"]="◯" if "音声通話" in col["func"] else ""
        col["sms"]="◯" if "SMS" in col["func"] else ""
        col["data"]="◯" if "データ通信" in col["func"] else ""

        # simの分割
        m=re.match("([^/]+)/([^/]+)",col["sim"])
        col["sim1"]=m.groups()[0].strip() if m else col["sim"]
        col["sim2"]=m.groups()[1].strip() if m else ""
        col=col.drop("sim")

        # プランの振り分け
        if "D" in col["plan"]:
            df_edited=df_edited.append(col,ignore_index=True)
        if "A" in col["plan"]:
            dfA_edited=dfA_edited.append(col,ignore_index=True)

    # カラムの並び替え
    #df_edited=df_edited.loc[:,['device_type', 'carrier', 'maker', 'name', 'model' 'os', 'sim', 'plan', 'LTE/3G', 'call', 'data', 'tethering', 'note']]

    df_edited.index.name="id"
    df_edited.to_csv(os.path.join(current_dir,"current/csv/devices_biglobeD-scraped-edited.csv"))

    dfA_edited.index.name="id"
    dfA_edited.to_csv(os.path.join(current_dir,"current/csv/devices_biglobeA-scraped-edited.csv"))


if __name__ == '__main__':

    postprocess()
