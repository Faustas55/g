#a basic script to export ad statistics from hades.db to a csv files which then goes to Splunk.
#set up as a scheduled task on the remote server
import datetime
import numpy as np
import pandas as pd
import sqlite3 as sql



#connecting to the database and selecting all ads
con=sql.connect(r"C:\Hades\HadesV2App\db\hades.db")
df_db = pd.read_sql("SELECT * FROM advert", con)

#exporting the database to splunk so we don't need to run the import script to get the data
df_db.to_csv(r"C:\Splunk\intel\hadesresults\hadesresults.csv")

#grouping by and cleaning the data
df_groupedby=df_db.groupby(['region','category']).size().unstack(level=1, fill_value=0).reset_index()
df_groupedby['authorised']=df_groupedby['authorised']+df_groupedby['syngenta authorised']
df_groupedby.drop(columns={'uncategorised\nuncategorised', 'syngenta authorised', 'archived'}, axis=1, inplace=True)

#adding the data so it's possible to timechart it
df_groupedby.loc[:, "uploaded_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#export
df_groupedby.to_csv(r"C:\Splunk\intel\hadesresults\hadesstatistics.csv", mode='a', header=False, index=False)
