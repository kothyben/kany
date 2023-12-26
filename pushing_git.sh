#!/bin/bash

#add commit and push one modification

read -p  "entrer le commentaire du commit : " cmt

git add .
git commit -m "$cmt"

read -p "branche sur laquelle faire le push : main ou master " branch

git push origin $branch
