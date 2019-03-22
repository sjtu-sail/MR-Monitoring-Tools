#!/usr/bin/env bash
export COLLECTOR_HOME="/home/wuchunghsuan/MR-Monitoring-Tools"
ids_file=${1##*/}
ids_file="$COLLECTOR_HOME/$ids_file"
work() {
	host=root@ist-slave$1
	tmp_file="/tmp/$2-$1"
	ssh $host 'bash -s' < $COLLECTOR_HOME/work_hc.sh $2 ${tmp_file}
	scp $host:$tmp_file $COLLECTOR_HOME/output/
	ssh $host "rm -f $tmp_file"
}
work_skew(){
    host=root@192.168.2.1$1
	tmp_file="/tmp/$2-$1"
	ssh $host 'bash -s' < $COLLECTOR_HOME/work_hc_skew.sh $2 ${tmp_file}
	scp $host:$tmp_file $COLLECTOR_HOME/output_skew/
	ssh $host "rm -f $tmp_file"
}

deal_single() {
    if [[ -n "$2" ]]; then
        for((i=1;i<=4;i++)); do
		    work_skew $i $1
	    done
    else
    	for((i=1;i<=4;i++)); do
		    work $i $1
	    done
    fi

}

if [ -z $1 ]; then
	echo "Usage: ${0##*/} app_id ---for draw map-reduce time
	            ${0##*/} app_id type(1:tasks,2:nodes) ---for fraw data skew   "
	exit 1
fi

#ids_file=${1##*/}
#ids_file="$COLLECTOR_HOME/$ids_file"
echo "debug: $ids_file"

for app_id in $(cat $ids_file); do
	echo
	echo "start pulling logs for job: $app_id"
	deal_single $app_id $2
done

echo
echo "pull log files finished."

if [[ -n "$2" ]]; then
    python $COLLECTOR_HOME/draw_skew.py $ids_file $2  2>errlog
else
    python $COLLECTOR_HOME/draw.py $ids_file 2>errlog
fi

if [ $? != 0 ]; then
	echo "error when drawing picture. view errlog for more infomation."
else
	echo "picture saved!"
	echo "done."
fi

