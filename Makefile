startmongo:
	mongod --dbpath data/ --port 1337 --fork --logpath data/log/mongo.db
run:
	ipython3 -i loganalyzer.py
