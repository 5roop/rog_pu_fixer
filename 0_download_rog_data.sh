curl --remote-name-all https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1992/ROG.zip

for f in $(ls *.zip)
do
    unzip $f
    rm $f
done