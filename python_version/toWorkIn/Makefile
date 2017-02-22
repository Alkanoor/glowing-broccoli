PULL_DIR=.
PUSH_DIR=../remote/files
KEY=../aes-operations/key

init:
	make -C ../remote init

init-existing-linux:
	make -C ../remote init-existing-linux

init-existing-windows:
	make -C ../remote init-existing-windows

push-no-check:
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR) $(KEY)
	make -C ../remote push

push:
	make -C ../remote pull
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR) $(KEY)
	make -C ../remote push

push-no-check-delete-useless:
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR) $(KEY) 1
	make -C ../remote push

push-delete-useless:
	make -C ../remote pull
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR) $(KEY) 1
	make -C ../remote push

pull:
	make -C ../remote pull
	python ../aes-operations/pullScript.py $(PUSH_DIR) $(KEY)
