work() {
	host=root@192.168.2.1$1
	tmp_file="/tmp/$2-$1"
	ssh $host 'bash -s' < /root/byWind/collector/work_hc.sh $2 ${tmp_file}
	scp $host:$tmp_file /root/byWind/collector/output/
	ssh $host "rm -f $tmp_file"
}

deal_single() {
	for((i=1;i<=4;i++)); do
		work $i $1
	done
}

if [ -z $1 ]; then
	echo "Usage: ${0##*/} app_id"
	exit 1
fi

ids_file=${1##*/}
ids_file="/root/byWind/collector/$ids_file"
echo "debug: $ids_file"

for app_id in $(cat $ids_file); do
	echo
	echo "start pulling logs for job: $app_id"
	deal_single $app_id
done

echo
echo "pull log files finished."

python /root/byWind/collector/draw.py $ids_file 2>errlog

if [ $? != 0 ]; then
	echo "error when drawing picture. view errlog for more infomation."
else
	echo "picture saved!"
	echo "done."
fi

