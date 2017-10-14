PULL_DIR=.
PUSH_DIR=../toPushIn
PUSH_DIR_FILES=../$(PUSH_DIR)/files
KEY=../aes-operations/key


config:
	make -C $(PUSH_DIR) config

init:
	make -C $(PUSH_DIR) init

init-existing-linux:
	make -C $(PUSH_DIR) init-existing-linux

init-existing-windows:
	make -C $(PUSH_DIR) init-existing-windows

push-no-check:
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR_FILES) $(KEY)
	make -C $(PUSH_DIR) push

push:
	make -C $(PUSH_DIR) pull
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR_FILES) $(KEY)
	make -C $(PUSH_DIR) push

push-no-check-delete-useless:
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR_FILES) $(KEY) 1
	make -C $(PUSH_DIR) push

push-delete-useless:
	make -C $(PUSH_DIR) pull
	python ../aes-operations/pushScript.py $(PULL_DIR) $(PUSH_DIR_FILES) $(KEY) 1
	make -C $(PUSH_DIR) push

pull:
	make -C $(PUSH_DIR) pull
	python ../aes-operations/pullScript.py $(PUSH_DIR_FILES) $(KEY)

remove-superficial:
	python ../aes-operations/removeScript.py $(PUSH_DIR_FILES) $(KEY)

update-locally:
	python ../aes-operations/pullScript.py $(PUSH_DIR_FILES) $(KEY)
