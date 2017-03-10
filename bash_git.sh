LATEST_TAG=$(git describe --tags --abbrev=0)
CURRENT_REVISION=$(git describe --tags)
FILES_CHANGED=$(git diff --name-only HEAD $LATEST_TAG)

for var in "${FILES_CHANGED[@]}"
do
        if [[ "$var" == "$SITE" ]]
        then
                echo $var $SITE
                VALID=1
        fi
done
