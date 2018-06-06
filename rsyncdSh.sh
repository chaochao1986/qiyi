#/bin/bash/


status=$(ps -ef|grep -E "rsync --daemon"|grep -v "grep")
pidFile=/var/run/rsyncd.pid
pid=$(pidof rsync)
start_rsyncd="rsync --daemon"

function rsyncdStart()
{
   if [ "X${status}" == "X" ];then
	rm -rf ${pidFile}
	${start_rsyncd}
	status1=$(ps -ef|grep -E "rsync --daemon"|grep -v "grep")
	if [ "X${status1}" != "X" ];then
		echo "rysncd is Running"
	fi
	
    else
	
	echo "rysncd is RunningA"
	
   fi



}


function rysncdStop()
{
  if [ "X${status}" != "X" ];then
	kill -9  $pid
	status2=$(ps -ef|grep -E "rsync --daemon"|grep -v "grep")
	if [ "X${status2}" == "X" ];then
		echo "rysncd is Stopping"
	fi
  else
	echo "rysncd is Stopping"
  fi


}


function rysncdStatus()
{
	if [ "X${status}" != "X" ];then
		echo "rysncd is Running"
	else
		echo "rysncd is Stopping"
	fi
}

function rysncdRestart()
{
	if [ "X$(status)" == "X" ];then
		rsyncdStart
	else
                rysncdStop
		rsyncdStart
	fi		

}


function main()
{

	case $1 in 
		start)
			rsyncdStart
			;;
		stop)
			rysncdStop
			;;
		restart)
			rysncdRestart
			;;
		status)
			rysncdStatus
			;;
		*)
			echo "Usage: $0 start|stop|restart|status"
			;;
	esac
}	

main $1	
