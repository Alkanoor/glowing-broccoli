PULL_DIR=.
PUSH_DIR=../toPushIn/files
KEY=../key

init:
	make -C ../toPushIn init

push-no-check:
	../pushScript.sh $(PULL_DIR) $(PUSH_DIR) $(KEY)
	make -C ../toPushIn push

push:
	make -C ../toPushIn pull
	../pushScript.sh $(PULL_DIR) $(PUSH_DIR) $(KEY)
	make -C ../toPushIn push

pull:
	make -C ../toPushIn pull
	../pullScript.sh $(PULL_DIR) $(PUSH_DIR) $(KEY)
