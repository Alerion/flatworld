.PHONY: all help startwebapp startfrontend generateworld createsuperuser updatejsmodules
	staticwatch migrate generatemapnikstyle generatetilestacheconf starttilestache
	staticclean staticbuild startdbserver removeworlds startpubsubproxy startgameserver
	generatebigworld

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: migrate - migrate DB and load fixtures.
migrate:
	python3 ./webapp/manage.py migrate
	python3 ./webapp/manage.py loaddata building

# target: savedata - save game data to fixtures.
savedata:
	python3 ./webapp/manage.py dumpdata --indent=4 building	> webapp/fixtures/building.json

# target: startwebapp - Start dev-server.
startwebapp: migrate
	python3 -u ./webapp/manage.py runserver 0.0.0.0:8000

# target: startfrontend - Start game-server.
startgameserver:
	python3 -u ./server/game.py

# target: startfrontend - Start frontend-server.
startfrontend:
	python3 -u ./server/frontend.py

# target: startpubsubproxy - Start 0mq proxy for PUB-SUB between fronted and game server.
startpubsubproxy:
	python3 -u ./server/pubsub_proxy.py

# target: startdbserver - Start DB-server.
startdbserver: migrate
	python3 -u ./server/db_server.py

# target: generateworld - Generate new World.
generateworld: migrate
	python3 ./webapp/manage.py generate_world

# target: generatebigworld - Generate new World with more points.
generatebigworld: migrate
	python3 ./webapp/manage.py generate_world --points=2000 --heights_map_width=2000 --hill_noise=true

# target: staticwatch - Remove all worlds.
removeworlds: migrate
	python3 ./webapp/manage.py remove_worlds

# target: createsuperuser - Create superuser.
createsuperuser: migrate
	python3 ./webapp/manage.py createsuperuser

# target: generatemapnikstyle - Generate Mapnik styles for all worlds.
generatemapnikstyle: migrate
	python3 ./webapp/manage.py generate_mapnik_style

# target: updatetilestacheconf - Update Tile Stache config.
generatetilestacheconf: migrate
	python3 ./webapp/manage.py generate_tilestache_conf

# target: starttilestache - Run Tile Stache server.
starttilestache: generatemapnikstyle generatetilestacheconf
	tilestache-server.py --ip 0.0.0.0 -c tilestache/tilestache.json

# target: updatejsmodules - Update node modules.
updatejsmodules:
	cd static && npm install && bower install --allow-root

# target: staticclean - Clean ./static/build.
staticclean:
	cd static && gulp clean

# target: staticbuild - Build static.
staticbuild: staticclean
	cd static && gulp build

# target: staticwatch - Watch static and build.
staticwatch: updatejsmodules staticbuild
	cd static && gulp

webappbash:
	docker-compose run --rm webapp /bin/bash

restartserver:
	docker-compose restart dbserver
	docker-compose restart game
	docker-compose restart frontend
