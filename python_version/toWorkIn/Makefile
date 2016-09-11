PULL_DIR=.
PUSH_DIR=../toPushIn/files
KEY=../aes-operations/key

init:
	make -C ../toPushIn init

push-no-check:
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR) $(KEY)
	make -C ../toPushIn push

push:
	make -C ../toPushIn pull
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR) $(KEY)
	make -C ../toPushIn push

push-no-check-delete-useless:
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR) $(KEY) 1
	make -C ../toPushIn push

push-delete-useless:
	make -C ../toPushIn pull
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR) $(KEY) 1
	make -C ../toPushIn push

pull:
	make -C ../toPushIn pull
	python ../aes-operations/pullScript.py $(PUSH_DIR) $(KEY)
