REPO=https://github.com/Alkanoor/removeDirectly.git

init:
	echo "Makefile">>.gitignore
	git config --global user.email "Alkanoor@github.com"
	git init
	git stage --all
	git commit -m "first commit"
	git remote add origin $(REPO)
	git push -u origin master

init-existing:
	echo "Makefile">>.gitignore
	git init
	git stage --all
	git commit -m "first commit"
	git push -u origin master

push:
	git stage --all
	git commit -m "répétition"
	git push

pull:
	git stash
	git pull origin master
