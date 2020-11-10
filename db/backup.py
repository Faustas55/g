import os
import time
import datetime
import pipes
import sys
sys.path.insert(1, '/Hades/HadesV2App/')
from config import username, password, database
# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
.
 
DB_HOST = 'localhost' 
DB_USER = username
DB_USER_PASSWORD = password
#DB_NAME = '/backup/dbnameslist.txt'
DB_NAME = database
BACKUP_PATH = '/backup'

# Getting current DateTime to create a separate backup folder
DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME
 
mysqldumppath=r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"

mysqldumppath= '"{}"'.format(mysqldumppath)
gzippath=r"C:\Program Files (x86)\GnuWin32\bin\gzip.exe"
gzippath='"{}"'.format(gzippath)

#mysqldump
db = DB_NAME
dumpcmd = mysqldumppath + " -h "  + DB_HOST + " -u " + DB_USER + " --password=" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
os.system(dumpcmd)

#zipping
gzipcmd = gzippath + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
os.system(gzipcmd)
