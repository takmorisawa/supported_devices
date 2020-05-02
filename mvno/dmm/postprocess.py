import pandas as pd
import os
import re

CARRIER_LIST=[
    "SIMフリー版",
    "docomo版",
    "au版",
    "SoftBank版"
]

def postprocess():

    current_dir=os.path.dirname(os.path.abspath(__file__))
    print("processing...{0}".format(current_dir))

    df=pd.read_csv(os.path.join(current_dir,"current/csv/devices_dmm-scraped.csv"),index_col=0)
    df=df.fillna("")
    df_edited=pd.DataFrame()


    for idx,row in df.iterrows():

        row["note"]=row["note"].replace("\n","")
        m=re.match(".*※(.+版)はSIMロックの解除が必要です。.*",row["note"])
        unlocks=re.findall("[^、]+版",m.groups()[0]) if m else []

        # simを分離
        m=re.match("(.+)\t(.+)",row["sim1"])
        row["sim1"]=m.groups()[0] if m else row["sim1"]
        row["sim2"]=m.groups()[1] if m else ""

        # carrierを分割
        carriers=row["name"].split("/")
        first = [item for item in CARRIER_LIST if item in carriers[0]]
        row["name"]=carriers[0].strip(first[0]).strip() if len(first)>0 else row["name"]
        carriers[0] = first[0] if len(first)>0 else ""

        # 行を追加する
        for carrier in carriers:
            row=row.copy()
            row["carrier"]=carrier
            row["unlock"]="必要" if carrier in unlocks else ""
            df_edited=df_edited.append(row,ignore_index=True)


    df_edited.index.name="id"
    df_edited.to_csv(os.path.join(current_dir,"current/csv/devices_dmm-scraped-edited.csv"))


if __name__ == '__main__':

    postprocess()
