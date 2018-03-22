REPO=https://github.com/Alkanoor/removeDirectly.git


config:
	git config --global user.email "Alkanoor@github.com"
	git config --global user.name "Alkanoor"

init: config
	echo "Makefile">>.gitignore
	git init
	git stage --all
	git commit -m "first commit"
	git remote add origin $(REPO)
	git push -u origin master

init-existing-linux:
	git init
	git remote add origin $(REPO)
	git pull origin --rebase master

init-existing-windows:
	git stash
	git pull origin --rebase master

push:
	git stage --all
	git commit -m "Repetition"
	git push

pull:
	git stash
	git pull origin master
