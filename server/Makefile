.PHONY: all help start_frontend

# target: all - Default target. Does nothing.
all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

# target: help - Display callable targets.
help:
	@egrep "^# target:" [Mm]akefile

# target: start_frontend - Start frontend server.
start_frontend:
	python frontend.py
