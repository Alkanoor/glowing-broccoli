REPO=https://github.com/Alkanoor/removeDirectly.git

init:
	echo "Makefile">>.gitignore
	git config --global user.email "Alkanoor@github.com"
	git config --global user.name "Alkanor"
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
	git commit -m "répétition"
	git push

pull:
	git stash
	git pull origin master

