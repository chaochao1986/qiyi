#/bin/bash/

Path=(/tmp /data/log /data/ads-backend-prod/export)

function ergodic(){
for file in `ls $1`
do
  if [ -d $1"/"$file ]
  then
	ergodic $1"/"$file 
  else
	local path=$1"/"$file	
	rm -rf  $path
  fi
done

}

main(){
 for tmp in ${Path[@]}
 do
 
   ergodic $tmp
done
		
}


main $*
