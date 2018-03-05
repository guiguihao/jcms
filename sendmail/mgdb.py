from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['pc']

send_mail = db['sendmail']
send_mail.ensure_index('mail', unique=True)

receive_mail = db['email']
receive_mail.ensure_index('data', unique=True)

record_mail = db['record']


    	 

