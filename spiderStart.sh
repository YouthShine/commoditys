#!/bin/bash
scrapyPath="/data/spider/commondity"
cd  ${scrapyPath}
starts=("haocaimao"
"ieou"
"makepolo"
"seton"
"deppre"
"wangshanggou"
"rolymro"
"zgw"
"hc360"
"ispek"
"gomro"
"315mro"
"btone-mro"
"gongchang"
"axmro"
"1ez"
"zkh360"
"vipmro"
"isweek"
"huaaomro"
"91yilong"
"iacmall"
"wwmro"
"grainger"
"mctmall"
"8shop"
"mrobay"
"ehsy"
"misumi-ec"
)
for i in ${starts[@]}; do
	while true;do
		iCnt=`ps -ef  | grep scrapy | grep -v grep|wc -l`
		if ((${iCnt}<10));
			then
				/usr/local/python2.7/bin/scrapy crawl ${i} > /dev/null 2>&1 &
				break
			else
				sleep 10m
		fi
	done
done
