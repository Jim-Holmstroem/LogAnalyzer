startmongo:
	mongod --dbpath data/ --port 1337 --fork --logpath data/log/mongo.db
run:
	python3 rssserver/rssserver.py
