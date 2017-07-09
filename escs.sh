##############################################################################
# clone, crocs, github.
cd ~/projects
git clone git@github.com:iogf/crocs.git crocs-code
##############################################################################
# push, crocs, github.
cd ~/projects/crocs-code
git status
git add *
git commit -a
git push 
##############################################################################
# create the develop branch, crocs.
git branch -a
git checkout -b development
git push --set-upstream origin development
##############################################################################
# merge master into development, crocs.
cd ~/projects/crocs-code
git checkout development
git merge master
git push
##############################################################################
# merge development into master, crocs.
cd ~/projects/crocs-code
git checkout master
git merge development
git push
git checkout development
##############################################################################
# check diffs, crocs.
cd ~/projects/crocs-code
git diff
##############################################################################
# delete the development branch, crocs.
git branch -d development
git push origin :development
git fetch -p 
##############################################################################
# undo, changes, crocs, github.
cd ~/projects/crocs-code
git checkout *
##############################################################################
# create, a new branch locally from an existing commit, from, master.
git checkout master
cd ~/projects/crocs-code
git checkout -b old_version fcebcd4f229cb29cac344161937d249785bf83f8
git push --set-upstream origin old_version

git checkout old_version
##############################################################################
# delete, old version, crocs.
git checkout master
git branch -d old_version
git push origin :old_version
git fetch -p 
##############################################################################
# create, toc, table of contents, crocs.
cd ~/projects/crocs-code
gh-md-toc BOOK.md > table.md
vy table.md
rm table.md
##############################################################################
# install, crocs.
sudo bash -i
cd /home/tau/projects/crocs-code
python2 setup.py install
rm -fr build
exit
##############################################################################
# build, crocs, package, disutils.
cd /home/tau/projects/crocs-code
python2.6 setup.py sdist 
rm -fr dist
rm MANIFEST
##############################################################################
# share, put, place, host, package, python, pip, application, crocs.

cd ~/projects/crocs-code
python2 setup.py sdist register upload
rm -fr dist
##############################################################################



