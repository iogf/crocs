##############################################################################
# Clone crocs.
cd ~/projects
git clone git@github.com:iogf/crocs.git crocs-code
##############################################################################
# Push code
cd ~/projects/crocs-code
git status
git add *
git commit -a
git push 
##############################################################################
# Create the development branch.
cd ~/projects/crocs-code
git branch -a
git checkout -b development
git push --set-upstream origin development
##############################################################################
# Merge master into development crocs.
cd ~/projects/crocs-code
git checkout development
git merge master
git push
##############################################################################
# Merge development into master crocs.
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
# install, crocs.
sudo bash -i
cd /home/tau/projects/crocs-code
python setup.py install
rm -fr build
exit
##############################################################################
# build, crocs, package, disutils.
cd /home/tau/projects/crocs-code
python2.6 setup.py sdist 
rm -fr dist
rm MANIFEST
##############################################################################
# Upload to pypi/pip.

cd ~/projects/crocs-code
python2 setup.py sdist register upload
rm -fr dist
##############################################################################
# check patch-1
cd /home/tau/projects/crocs-code/
git checkout -b cclauss-patch-1 master
git pull https://github.com/cclauss/crocs.git patch-1

# Merge pull request.
git checkout development
git merge --no-ff cclauss-patch-1
git push origin development





