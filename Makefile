.PHONY: all help startwebapp startfrontend generateworld createsuperuser updatejsmodules
	staticwatch migrate generatemapnikstyle generatetilestacheconf starttilestache
	staticclean staticbuild

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: migrate - migrate DB.
migrate:
	python3 ./webapp/manage.py migrate

# target: startwebapp - Start dev-server.
startwebapp: migrate
	python3 ./webapp/manage.py runserver 0.0.0.0:8000

# target: startfrontend - Start frontend-server.
startfrontend: migrate
	python3 ./server/frontend.py

# target: generateworld - Generate new World.
generateworld: migrate
	python3 ./webapp/manage.py generate_world

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
