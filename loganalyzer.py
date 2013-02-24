import pymongo
from time import strptime as time_parser
import os

log_file = "/var/log/syslog.1"
assert(os.path.isfile(log_file))
mongocollection = {
    'database': 'logfiles',
    'name': log_file
}

def parser(line):
    month, day, time, domain, sndr, *msg = line.split()
    sender, *number = sndr.rstrip(':').rstrip(']').split('[') #``sender[number]'' OR ``sender''
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

with open(log_file) as logf, pymongo.MongoClient('localhost', 1337) as mongoconn:
    mongod = mongoconn[mongocollection['database']]
    logdata = map(parser,logf)
    data = mongod[mongocollection['name']]
    data.remove()
    data.insert(
        map(
            parser,
            logf
        )
    )

def sender_statistics(data, sender):
    """returns an senders data"""
    sender_data = list(data.find({'sender': sender}))
    return dict( #sender statistics
        count=data.find({'sender': sender}).count(),
        data=sender_data
    )

senders = dict(
    map(
        lambda sender: 
            (
                sender,
                sender_statistics(data, sender)
            ),
        data.distinct('sender')
    )
)

def render_sender(sender):
    #need some clusterings to group together things which only differ on irrelevant data like [0.0001]
    for line in senders[sender]['data']: 
        print(line['message'])
