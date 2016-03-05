PULL_DIR=.
PUSH_DIR=../toPushIn/files
KEY=../key

init:
	make -f ../toPushIn/Makefile init

push:
	make -f ../toPushIn/Makefile pull
	../pushScript.sh $(PULL_DIR) $(PUSH_DIR) $(KEY)
	make -f ../toPushIn/Makefile push

pull:
	make -f ../toPushIn/Makefile pull
	../pullScript.sh $(PULL_DIR) $(PUSH_DIR) $(KEY)
