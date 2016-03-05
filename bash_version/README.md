# Encrypt your repo

## Goal

You want to protect dir X for beeing seen.

## Instructions

* Create a parent folder which will contain folder X, a secret key that you create and save in this parent folder, and a child folder which will contain pushed ref.
* In the makefile of folder X, copy the push and pull instructions that are in the makefile of the folder toWorkIn here.
* Change the options of this makefile in order to be coherent with the name of your key file and folder.
* Copy the pullScript.sh, the pushScript.sh in this folder.
* Copy the makefile in toPushIn in the child folder you created (which contain encrypted files).
* Create a remote repository.
* Modify makefile in created child folder this way.
* Type make init in your main folder, then you could type make push (or make push-no-check => if you want to modify the makefile) if you want to update the folder remotely or make pull if you want to update it locally.

## Warnings

* Don't lose or modify the key if you want to be able to recover previous commits made.
* Keep the key secret or all that is useless.
