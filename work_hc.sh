# arg1: app_id
# arg2: output_filepath
dir_path=/root/log/nodemanager/$1

tmp_file=${2}
if [ -e $tmp_file ]; then
	rm -f $tmp_file
fi
touch $tmp_file

for dir in `ls $dir_path`; do 
	if [ -d $dir_path/$dir ]; then
		cat $dir_path/$dir/syslog | grep -F "[IST]" >> $tmp_file
	fi
done

