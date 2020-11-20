wavdir="123 45"
echo $wavdir
cd "$wavdir"

for i in "$wavdir"/*; do
 echo $i
done
