# Encrypt your repo

## Goal

You want to protect dir X for beeing seen.

## Instructions

* Create a parent folder which will contain dir X
* Create another dir in this parent dir, which will contain pushed ref. Create a "files" directory inside
* Copy the "aes-operations" directory again in the parent one
* Modify the key inside "aes-operations"
* Copy the makefile in toPushIn in the child folder you created (which contain encrypted files, so near the "files" dir)
* Copy the makefile in toWorkIn in your X folder (or add targets in your current makefile if you have one)
* Type make init in your X folder, then you could type make-push if you want to update the folder remotely or make pull if you want to update it locally.

## Warnings

* Don't lose or modify the key if you want to be able to recover previous commits made.
* Keep the key secret or all that is useless.
