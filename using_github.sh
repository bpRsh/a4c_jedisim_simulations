#!bash

# $1 is first argument
REPO='a4a_lsst_jedisim_301gals'
echo "Copying $1"
mv ../1$REPO/$1 ./$1 &&
git add $1 &&
git commit -am "added $1" &&
git push origin master
