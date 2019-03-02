import pandas as pd
import os
import re

def postprocess():

    current_dir=os.path.dirname(os.path.abspath(__file__))
    print("processing...{0}".format(current_dir))

    df=pd.read_csv(os.path.join(current_dir,"current/csv/devices_nifmo-scraped.csv"),index_col=0)
    df_edited=pd.DataFrame()

    for idx,col in df.iterrows():

        tmp_name=col["name"].replace("\n","").replace("™","")

        m=re.match(".*機種名：\t([^\t]+).*",tmp_name)
        col["name"]=m.groups()[0].strip() if m else ""

        m=re.match("(.+)／(.+)",col["sim1"])
        col["sim1"]=m.groups()[0].strip() if m else col["sim1"]
        col["sim2"]=m.groups()[1].strip() if m else ""

        for carrier in col["carrier"].split("/"):
            col=col.copy()
            col["carrier"]=carrier
            df_edited=df_edited.append(col,ignore_index=True)

    df_edited.index.name="id"
    df_edited.to_csv(os.path.join(current_dir,"current/csv/devices_nifmo-scraped-edited.csv"))


if __name__ == '__main__':

    postprocess()
