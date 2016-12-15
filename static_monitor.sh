num=`ps -ef|grep spider_redisStart|grep -v grep |wc -l`
if [ $num==0 ];then
	/data/spider/commondity/static_monitor.sh
fi
