REPO=https://github.com/Alkanoor/removeDirectly.git

init:
	cd files
	git init
	@git stage --all
	@git commit -m "first commit"
	@git remote add origin $(REPO)
	git push -u origin master
	cd ..

push:
	cd files
	@git stage --all
	@git commit -m "répétition"
	git push
	cd ..

pull:
	cd files
	@git stash
	git pull
	cd ..
