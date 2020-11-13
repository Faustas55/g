import os
import time
import datetime
import pipes
import sys
sys.path.insert(1, '/Hades/HadesV2App/')
from configforbackup import username, password, database
# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.
 
DB_HOST = 'localhost' 
DB_USER = username
DB_USER_PASSWORD = password
#DB_NAME = '/backup/dbnameslist.txt'
DB_NAME = database
BACKUP_PATH = '/backup'

# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME
 
# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.makedirs(TODAYBACKUPPATH)

mysqldumppath=r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"

mysqldumppath= '"{}"'.format(mysqldumppath)
gzippath=r"C:\Program Files (x86)\GnuWin32\bin\gzip.exe"
gzippath='"{}"'.format(gzippath)
# Starting actual database backup process.

db = DB_NAME
dumpcmd = mysqldumppath + " -h "  + DB_HOST + " -u " + DB_USER + " --password=" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"

os.system(dumpcmd)
gzipcmd = gzippath + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
os.system(gzipcmd)

