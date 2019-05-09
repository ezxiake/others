echo "shell dict"

declare -A dic
dic=([key1]="value1" [key2]="value2" [key3]="value3")

#print value of the key
echo ${dic["key1"]}
#print all of keys
echo ${!dic[*]}
#print all of value
echo ${dic[*]}
#add a new element into the dict
dic+=([key4]="value4")

#Iteratively print the value of the key
for key in $(echo ${!dic[*]})
do
    echo "$key : ${dic[$key]}"
done

echo "shell array"

#array
list=("value1" "value2" "value3")
#print value of subscript
echo ${list[1]}
#print all of subscript
echo ${!list[*]}
#print all of element
echo ${list[*]}
#add a new element into the array
list=("${list[@]}" "value4")

for i in "${!list[@]}"; do 
    printf "%s\t%s\n" "$i" "${list[$i]}"
done

for NUM in ${list[*]}
do
    echo $NUM
done