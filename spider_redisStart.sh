#!/bin/bash
scrapyPath="/data/spider/commondity"
cd  ${scrapyPath}
starts=(
"spider_ehsy_redis"
"spider_wwmro_redis"
"spider_iacmall_redis"
"spider_sssmro_redis"
"spider_grainger_redis"
"spider_axmro_redis"
"spider_ispek_redis"
"spider_zkh360_redis"
"spider_gongchang_redis"
"spider_mrobay_redis"
"spider_wangshanggou_redis"
"spider_315mro_redis"
"spider_makepolo_redis"
"spider_huaaomro_redis"
"spider_gomro_redis"
"spider_hc360_redis"
"spider_1ez_rediss"
"spider_mctmall_redis"
"spider_btone-mro_redis"
"spider_rolymro_redis"
"spider_isweek_redis"
"spider_vipmro_redis"
"spider_deppre_redis"
"spider_8shop_redis"
"spider_ieou_redis"
"spider_seton_redis"
"spider_91yilong_redis"
"spider_haocaimao_redis"
)
for i in ${starts[@]}; do
	while true;do
		iCnt=`ps -ef  | grep scrapy | wc -l`
		iCnt=`expr ${iCnt} - 1`
		if ((${iCnt}<10));
			then
				/usr/local/python2.7/bin/scrapy crawl ${i} > /dev/null 2>&1 &
				break
			else
				sleep 10m
		fi
	done
done
