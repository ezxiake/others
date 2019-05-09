#Function lists
#  bakMysql
#  bakRedis
#  bakApp
#  installMysql
#  installRedis
#  installRdssApp
#  rollbackMysql
#  Rollbackredis
#  rollbackRdssApp

#备份mysql数据库
bakMysql(){
#echo "未开通"
	#curdate="20170106"
	echo "开始备份数据库相关..."
	cd /oper/bak
	mysqldump -urds -prds -h127.0.0.1 RDS_DB XIAOKE > /oper/bak/XIAOKE.sql
	sleep 2
	echo "备份完成！"
#	su - weblogic -c mkdir -p /oper/bak/backup$curdate
#	su - weblogic -c exp $etellerDbConnect tables=$(cat /oper/install/update$curdate/etellerTablesBak.txt) file=/oper/bak/backup$curdate/eteller$curdate.dmp log=$bakEtellerDblog
#	echo "备份受理中心数据库(eteller)结束"
#	ts=`date +'%Y-%m-%d.%H:%M:%S'`
#	echo "$ts 备份受理中心数据库(eteller)结束">>$log
}

#备份redis数据库
bakRedis(){
echo "未开通"
#	su - weblogic -c mkdir -p /oper/bak/backup$curdate
#	su - weblogic -c exp $autekDbConnect tables=$(cat /oper/install/update$curdate/autekTablesBak.txt) file=/oper/bak/backup$curdate/autek$curdate.dmp log=$bakBcomsDblog
#	echo "备份作业中心数据库(autek)结束"
#	ts=`date +'%Y-%m-%d.%H:%M:%S'`
#	echo "$ts 备份作业中心数据库(autek)结束">>$log
}

#备份应用
bakApp(){

	oper_date="20170106"
	echo "新建备份文件夹:backup$oper_date"

	ts=`date +'%Y-%m-%d.%H:%M:%S'`
	echo "$ts 新建备份文件夹:backup$oper_date">>$log

	su - weblogic -c "mkdir -p /oper/bak/backup$oper_date"

	echo "复制工程rds_app到新文件夹中"

	ts=`date +'%Y-%m-%d.%H:%M:%S'`
	echo "$ts 复制工程rds_app到新文件夹中">>$log

#	su - weblogic -c cp -r /weblogic/upload/bcoms /oper/bak/backup$oper_date/
	su - weblogic -c "tar -zcvf /oper/bak/backup$oper_date/rds_app_${oper_date}_backup.tar.gz /weblogic/rds_app/rds*"

	echo "============作业中心应用备份结束===================="

	ts=`date +'%Y-%m-%d.%H:%M:%S'`
	echo "$ts ============作业中心应用备份结束====================">>$log

}

#部署mysql数据库脚本
installMysql(){

#	su - mysql -c "mkdir -p /rdsdata/share/dwdata/backup;mkdir -p /rdsdata/share/dwdata/history;mkdir -p /rdsdata/share/dwdata/tmpfile;mkdir -p /mysql/dw_script"
#	su - mysql -c "cd /rdsdata/share;chown -R mysql:mysql dwdata;chmod -R 777 dwdata"
#	su - mysql -c "cd /mysql;chown -R mysql:mysql dw_script;chmod -R 755 dw_script"

#	ls -l /mysql|grep dw_script
#	ls -l /rdsdata/share/dwdata/
#	echo "目录创建"
#	ts=`date +'%Y-%m-%d.%H:%M:%S'`
#	echo "$ts 目录创建结束">>$log
#	su - weblogic -c "cd /oper/install;unzip -o ${oper_date}"
#	su - weblogic -c sqlplus $etellerDbConnect @/oper/install/update$curdate/EtellerDbList.sql|tee -a $installEtellerDblog

#		解压投产包
	oper_date="20170106"
	su - weblogic -c "cd /oper/install;unzip -o ${oper_date}"
	cd /oper/install/${oper_date}/
	chmod -R 777 *
	echo "解压完成，准备开始部署..."
	sleep 1

	cd /oper/install/${oper_date}/sql
	mysql -h127.0.0.1 -u${mysql_user} -p${mysql_pwd} RDS_DB < mysql_init_RDS_DB_20170106.sql
	echo "1/1 mysql -h127.0.0.1 -u${mysql_user} -p${mysql_pwd} RDS_DB < mysql_init_RDS_DB_20170106.sql 执行完毕"
	
#	mysql -h127.0.0.1 -uroot -proot < mysql_init_20160520_guize_REP_DB.sql
#	echo "2/2 mysql -h127.0.0.1 -uroot -proot < mysql_init_20160520_guize_REP_DB.sql 执行完毕"
#	mysql -h127.0.0.1 -u${mysql_user} -p${mysql_pwd} -D ${mysql_dbn} -e "SELECT t.TABLE_NAME,t.TABLE_ROWS FROM information_schema.TABLES t WHERE t.TABLE_SCHEMA = 'RDS_DB' AND t.TABLE_NAME IN ('T01_D_EAS_PTY_PRD_BAL','T01_D_EAS_PTY_PRD_BAL_REPAIR','T01_D_EAS_RATE_INFO','T01_D_EAS_RATE_INFO_REPAIR','T011_D_EAS_PRD_AGGR_INCO','T011_D_EAS_PTY_PRD_AGGR_INCO','T11_LOAD_DES_PKCONF','T11_RES_TAB','T10_REALTIME_DATA_EXTRACT_CONF');"
#	mysql -h127.0.0.1 -uroot -proot -D ${mysql_dbn} -e "SELECT * FROM information_schema.INNODB_SYS_INDEXES WHERE SUBSTR(NAME,1,7) = 'INDEX_T';"
#	mysql -h127.0.0.1 -u${mysql_user} -p${mysql_pwd} -D ${mysql_dbn} -e "show procedure status like \"P01_APP_REALTIME_ETL%\"\G;"
#	mysql -h127.0.0.1 -u${mysql_user} -p${mysql_pwd} -D ${mysql_dbn} -e "SELECT TRAN_CODE,ZX_ADDR,FLAG FROM RDS_DB.T10_REALTIME_DATA_EXTRACT_CONF ORDER BY TRAN_CODE;"
#	mysql -h127.0.0.1 -u${mysql_user} -p${mysql_pwd} -D RDS_WEB_DB -e "SELECT t.TABLE_NAME,t.TABLE_ROWS FROM information_schema.TABLES t WHERE t.TABLE_SCHEMA = 'RDS_WEB_DB';"
# | tee -a ${installMysqlDblog}
	echo "部署mysql数据库脚本结束"
	ts=`date +'%Y-%m-%d.%H:%M:%S'`
	echo "$ts 部署mysql数据库脚本结束">>$log

}

#部署redis数据库脚本
installRedis(){

# su - weblogic -c sqlplus $autekDbConnect @/oper/install/update$curdate/AutekDbList.sql|tee -a $installAutekDblog
	oper_date="20170106"  #xlx#
	cd /oper/install/${oper_date}/sql
	chmod -R 777 *
# sh redis_ini.sh redis_init_20160422 0 11.1.3.60 6379
	sh redis_ini.sh redis_init_20170106 0 ${redis_host} 6379
	echo "1/1 redis_init_20170106 执行完毕!"

#	sh redis_ini.sh redis_init_20160520_huidan_merge 0 ${redis_host} 6379
#	echo "2/3 redis_init_20160520_huidan_merge 执行完毕!"
#	sh redis_ini.sh redis_init_20160520_shucang_choushu 0 ${redis_host} 6379
#	echo "3/3 redis_init_20160520_shucang_choushu 执行完毕!"
#	cat ${redis_init_file_name}|/mysql/dw_script/redis-cli --raw -a ${redis_pwd} -h ${redis_host} -p ${redis_port} -n ${redis_db_num}|tee -a ${installRedisDblog}
  echo "部署redis数据库脚本结束"
  ts=`date +'%Y-%m-%d.%H:%M:%S'`
  echo "$ts 部署redis数据库脚本结束">>$log

}

#部署oracle数据库脚本
installOracle(){
echo "未开通"
# su - weblogic -c sqlplus $autekDbConnect @/oper/install/update$curdate/AutekDbList.sql|tee -a $installOracleDblog
#	su - weblogic -c "cd /oper/install/${oper_date};sqlplus ${oracle_user}/${oracle_password}@${oracle_host}:${oracle_port}/${oracle_service_name} @${oracle_init_file_name} |tee -a ${installOracleDblog}"
#  echo "部署oracle数据库脚本结束"
#  ts=`date +'%Y-%m-%d.%H:%M:%S'`
#  echo "$ts 部署oracle数据库脚本结束">>$log
}

#部署RDSS应用
installRdssApp(){

# 请修改该处日期为上线日期————文件包解压后的日期目录
	oper_date="20170106"

	has=0
	for file in $(ls /oper/bak/backup${oper_date}/)
	do
		if [ "$file" = "rds_app_${oper_date}_backup.tar.gz" ];then
				has=1
		fi
	done

	if [ $has = 1 ];then

		##############################
		#   以下请填写上线部署代码   #
		##############################

#		su - weblogic -c "mkdir -p /rdsdata/share/ybdata;mkdir -p /weblogic/rds_app/rds_yb_query"
#		su - weblogic -c "cd /weblogic/rds_app;chown -R weblogic:bea rds_yb_query;chmod -R 755 rds_yb_query"
#		su - weblogic -c "\cp -r /oper/install/${oper_date}/rds_file_share.sh /weblogic/rds_app/rds_yb_query"
#		su - weblogic -c "cd /weblogic/rds_app/rds_rde/config/;\cp scheduler.xml scheduler.xml_20160513"
#		su - weblogic -c "rm -rf /weblogic/rds_app/rds_rde/lib/*"

#		拷贝rds_app工程文件到/weblogic目录
#		su - weblogic -c "\cp -r /oper/install/${oper_date}/rds_app /weblogic"
#		解压war包
#		su - weblogic -c "cd /weblogic/rds_app/rds_http_rep/;unzip -o rds_http_rep.war"
#		su - weblogic -c "cd /weblogic/rds_app/rds_rep/;unzip -o rds_rep.war"

#		cd /weblogic/rds_app/rds_rde/config
#		cp -r scheduler.xml scheduler.xml20160722
#		cp -r trans_elemet_mapping.txt trans_elemet_mapping.txt20160722
#		cd /oper/install/20160722/rds_app/rds_rde/config
#		cp -r scheduler.xml /weblogic/rds_app/rds_rde/config
#		cp -r trans_elemet_mapping.txt /weblogic/rds_app/rds_rde/config

####################################################
#		清除weblogic缓存
#		su - weblogic -c "rm -rf /weblogic/app/user_projects/domains/rds_domain/servers/AdminServer/tmp/_WL_user/*"

#		解压投产包
		su - weblogic -c "cd /oper/install;unzip -o ${oper_date}"
		cd /oper/install/${oper_date}/
		chmod -R 777 *
		echo "解压完成，准备开始部署..."
		sleep 3

		su - weblogic -c "cd /oper/install/${oper_date}/rds_app;cp -r build.jar /weblogic/rds_app/rds_dwb/lib"
		su - weblogic -c "cd /oper/install/${oper_date}/rds_app;cp -r execute.jar /weblogic/rds_app/rds_dwb/lib"
		su - weblogic -c "cd /oper/install/${oper_date}/rds_app;cp -r packet.jar /weblogic/rds_app/rds_dwb/lib"
		su - weblogic -c "cd /oper/install/${oper_date}/rds_app;cp -r parse.jar /weblogic/rds_app/rds_dwb/lib"
		su - weblogic -c "cd /oper/install/${oper_date}/rds_app;cp -r sqlparse.jar /weblogic/rds_app/rds_dwb/lib"
		su - weblogic -c "cd /oper/install/${oper_date}/rds_app;cp -r scheduler.jar /weblogic/rds_app/rds_rde/lib"
		su - weblogic -c "cd /oper/install/${oper_date}/rds_app;cp -r license.xml /weblogic/rds_app/rds_web/WEB-INF/classes"
#		rds_app目录递归赋权限
		chmod -R 755 /weblogic/rds_app/
echo "解压zip包成功，赋权755成功"

####################################################
#		#检查后台sh是否开启
#		prd_ip=`ifconfig |grep 11.1.3.56`
#		uat_ip=`ifconfig |grep 10.1.89.75`
#		other_ip=`ifconfig |grep 10.1.87.49`
#		if [ "${prd_ip}" != "" -o "${uat_ip}" != "" -o "${other_ip}" != "" ]; then
#			su - weblogic -c "cd /weblogic/rds_app/rds_rde/;sh start_CheckSchedulerStatus.sh"
#			sleep 3
#			ps -ef |grep CheckSchedulerStatus
#	  fi

#		删除3.240的无用程序 删除56/57无用的程序
#		prd_ip_228=`ifconfig |grep 10.1.89.228`
#		if [ "${prd_ip_228}" != "" ]; then
#			echo "228上测试su - weblogic -c rm -r /weblogic/rds_app/xxxxxx语句"
#			su - weblogic -c "touch /weblogic/rds_app/test"
#			su - weblogic -c "ls -lrt /weblogic/rds_app/"
#			su - weblogic -c "rm -r /weblogic/rds_app/test"
#			su - weblogic -c "ls -lrt /weblogic/rds_app/"
#			sleep 1
#			echo "sh /weblogic/rds_app/rds_dwb/start_all.sh 准备重新加载总线应用..."
#			sleep 1
#			su - weblogic -c "sh /weblogic/rds_app/rds_dwb/start_all.sh"
#		fi
#		prd_ip_240=`ifconfig |grep 11.1.3.240`
#		if [ "${prd_ip_240}" != "" ]; then
#			su - weblogic -c "rm -r /weblogic/rds_app/rds_rde"
#			su - weblogic -c "rm -r /weblogic/rds_app/rds_http_rep"
#			sleep 1
#		fi
#		prd_ip_56=`ifconfig |grep 11.1.3.56`
#		if [ "${prd_ip_56}" != "" ]; then
#			su - weblogic -c "rm -r /weblogic/rds_app/rds_rep"
#			sleep 1
#			echo "sh /weblogic/rds_app/rds_dwb/start_all.sh 准备重新加载总线应用..."
#			sleep 1
#			su - weblogic -c "sh /weblogic/rds_app/rds_dwb/start_all.sh"
#		fi
#		prd_ip_57=`ifconfig |grep 11.1.3.57`
#		if [ "${prd_ip_57}" != "" ]; then
#			su - weblogic -c "rm -r /weblogic/rds_app/rds_rep"
#			sleep 1
#			echo "sh /weblogic/rds_app/rds_dwb/start_all.sh 准备重新加载总线应用..."
#			sleep 1
# 		su - weblogic -c "sh /weblogic/rds_app/rds_dwb/start_all.sh"
#		fi

		##############################
		#   以上请填写上线部署代码   #
		##############################

		echo "部署RDSS应用结束"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 部署RDSS应用结束">>$log
	else
		echo "部署RDSS应用失败，请先备份RDSS应用"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 部署RDSS应用失败，请先备份RDSS应用">>$log
	fi

}

#回滚mysql数据库
rollbackMysql(){

echo "开始回滚..."
cd /oper/bak
mysql -urds -prds RDS_DB <<EOF
source /oper/bak/XIAOKE.sql
EOF

echo "回滚完成！"

#echo "未开通"
#	has=0
#	for file in $(ls /oper/bak/backup$curdate/)
#	do
#		if [ $file = eteller ]
#			then
#				has=1
#		fi
#	done
#	if [ $has = 1 ]
#		then
#		su - weblogic -c rm -rf /weblogic/upload/eteller
#		su - weblogic -c cp -r /oper/bak/backup$curdate/eteller /weblogic/upload/
#		echo "回滚受理中心应用(eteller)成功"
#		ts=`date +'%Y-%m-%d.%H:%M:%S'`
#		echo "$ts 回滚受理中心应用(eteller)成功">>$log
#	else
#		echo "回滚受理中心应用(eteller)失败，不存在备份文件"
#		ts=`date +'%Y-%m-%d.%H:%M:%S'`
#		echo "$ts 回滚受理中心应用(eteller)失败，不存在备份文件">>$log
#	fi
}

#回滚redis数据库
rollbackRedis(){
echo "未开通"
#	has=0
#	for file in $(ls /oper/bak/backup$curdate/)
#	do
#		if [ $file = bcoms ]
#			then
#				has=1
#		fi
#	done
#	if [ $has = 1 ]
#		then
#		su - weblogic -c rm -rf /oper/bak/bcoms
#		su - weblogic -c cp -r /oper/bak/backup$curdate/bcoms /weblogic/upload/
#		echo "回滚作业中心应用(bcoms)成功"
#		ts=`date +'%Y-%m-%d.%H:%M:%S'`
#		echo "$ts 回滚作业中心应用(bcoms)成功">>$log
#	else
#		echo "回滚作业中心应用(bcoms)失败，不存在备份文件"
#		ts=`date +'%Y-%m-%d.%H:%M:%S'`
#		echo "$ts 回滚作业中心应用(bcoms)失败，不存在备份文件">>$log
#	fi
}

#回滚受理中心应用(eteller)
rollbackRdssApp(){
	curdate="20170106"
	cd /oper/bak/backup$curdate
	backFileName="rds_app_${curdate}_backup.tar.gz"
	if [ -e ${backFileName} ] ; then
		echo "存在${backFileName}"
		cp -r ${backFileName} /weblogic
		cd /weblogic
		echo "开始解压${backFileName}..."
		su - weblogic -c "tar -zxvf rds_app_${curdate}_backup.tar.gz"
		sleep 2
		rm -r rds_app_${curdate}_backup.tar.gz
		echo "回滚完成！"
	else
		echo "不存在${backFileName}"
	fi
#echo "未开通"
#	has=0
#	for file in $(ls /oper/bak/backup$curdate/)
#	do
#		if [ $file = eteller ]
#			then
#				has=1
#		fi
#	done
#	if [ $has = 1 ]
#		then
#		su - weblogic -c rm -rf /weblogic/upload/eteller
#		su - weblogic -c cp -r /oper/bak/backup$curdate/eteller /weblogic/upload/
#		echo "回滚受理中心应用(eteller)成功"
#		ts=`date +'%Y-%m-%d.%H:%M:%S'`
#		echo "$ts 回滚受理中心应用(eteller)成功">>$log
#	else
#		echo "回滚受理中心应用(eteller)失败，不存在备份文件"
#		ts=`date +'%Y-%m-%d.%H:%M:%S'`
#		echo "$ts 回滚受理中心应用(eteller)失败，不存在备份文件">>$log
#	fi
}

