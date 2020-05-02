import pandas as pd
import os
import re

plan_docomo="タイプD/ドコモ網"
plan_au="タイプA/au網"

def postprocess():

    current_dir=os.path.dirname(os.path.abspath(__file__))
    print("processing...{0}".format(current_dir))

    df=pd.read_csv(os.path.join(current_dir,"current/csv/devices_iij-scraped.csv"),index_col=0)
    df_edited=pd.DataFrame()
    dfA_edited=pd.DataFrame()

    for idx,col in df.iterrows():

        # name, carrier
        m=re.match("\['(.+)', '(.+)'\]",col["name"])
        col["name"]=m.groups()[0] if m else col["name"]
        carrier_list=m.groups()[1].split("/") if m else [""]

        m=re.match("\['(.+)'\]",col["name"])
        col["name"]=m.groups()[0] if m else col["name"]

        col["name"]=col["name"].replace("\\u2003","")
        col["maker"]=col["maker"].replace("\u2003","")

        m=re.match("(.+)\xa0x\xa02",col["sim"])
        col["sim1"]=m.groups()[0] if m else col["sim"]
        col["sim2"]=m.groups()[0] if m else ""
        col=col.drop("sim")


        for carrier in carrier_list:

            col["carrier"]=carrier

            # planの振り分け
            if col["plan"]==plan_docomo:
                df_edited=df_edited.append(col,ignore_index=True)
            elif col["plan"]==plan_au:
                dfA_edited=dfA_edited.append(col,ignore_index=True)
            else:
                pass

    df_edited.index.name="id"
    df_edited.to_csv(os.path.join(current_dir,"current/csv/devices_iijD-scraped-edited.csv"))
    dfA_edited.index.name="id"
    dfA_edited.to_csv(os.path.join(current_dir,"current/csv/devices_iijA-scraped-edited.csv"))


if __name__ == '__main__':

    postprocess()
