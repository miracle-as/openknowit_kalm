ign8_bump patch
MYMESSAGE=$(git status)
git commit -a -m  "$MYMESSAGE"
git push 
rm poetry.lock
rm -r dist || echo
poetry update
poetry build
poetry run twine upload dist/* || echo
#curl -X POST ${IGN8_JENKINS_URL}/job/ign8/build \
#  --user jho:${IGN8_JENKINS_TOKEN}

