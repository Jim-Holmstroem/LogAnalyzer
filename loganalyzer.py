import pymongo
from time import strptime as time_parser
import os


log_file = "/var/log/syslog"
assert(os.path.isfile(log_file))
mongocollection = {
    'database': 'logfiles',
    'name': log_file
}

def parser(line):
    month, day, time, domain, sndr, *msg = line.split()
    sender = sndr.rstrip(':')
    message = ' '.join(msg)
    return dict(
        datatime=time_parser(
            "{day};{month};13;{time}".format(
                month=month,
                day=day,
                time=time,
            ),
            '%d;%b;%y;%H:%M:%S' #'day;month;year;hour:minute:second'
        ),
        domain=domain,
        sender=sender,
        message=message
    )

#ugly put it's supposed to run interactivly and thus needs a handle to the mongo open after execution.
mongoconn = pymongo.MongoClient('localhost', 1337) 
with open(log_file) as logf:#, pymongo.MongoClient('localhost', 1337) as mongoconn:
    mongod = mongoconn[mongocollection['database']]
    logdata = map(parser,logf)
    mongoc = mongod[mongocollection['name']]
    mongoc.remove()
    mongoc.insert(
        map(
            parser,
            logf
        )
    )

