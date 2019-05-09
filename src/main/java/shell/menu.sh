#!/bin/bash
source /oper/install/rdss_comm.sh

oper_date=`date +%Y%m%d`
rds_activemq_path=`awk 'FS="="{if($0~/^rds_activemq_path/) print $2}' /oper/install/rdss_config.ini`
rds_weblogic_path=`awk 'FS="="{if($0~/^rds_weblogic_path/) print $2}' /oper/install/rdss_config.ini`
rds_dwb_path=`awk 'FS="="{if($0~/^rds_dwb_path/) print $2}' /oper/install/rdss_config.ini`
rds_app_log_path=`awk 'FS="="{if($0~/^rds_app_log_path/) print $2}' /oper/install/rdss_config.ini`
mysql_host=`awk 'FS="="{if($0~/^mysql_host/) print $2}' /oper/install/rdss_config.ini`
mysql_user=`awk 'FS="="{if($0~/^mysql_user/) print $2}' /oper/install/rdss_config.ini`
mysql_pwd=`awk 'FS="="{if($0~/^mysql_pwd/) print $2}' /oper/install/rdss_config.ini`
mysql_dbn=`awk 'FS="="{if($0~/^mysql_dbn/) print $2}' /oper/install/rdss_config.ini`
redis_host=`awk 'FS="="{if($0~/^redis_host/) print $2}' /oper/install/rdss_config.ini`
redis_port=`awk 'FS="="{if($0~/^redis_port/) print $2}' /oper/install/rdss_config.ini`
redis_db_num=`awk 'FS="="{if($0~/^redis_db_num/) print $2}' /oper/install/rdss_config.ini`
redis_pwd=`awk 'FS="="{if($0~/^redis_pwd/) print $2}' /oper/install/rdss_config.ini`
oracle_host=`awk 'FS="="{if($0~/^oracle_host/) print $2}' /oper/install/rdss_config.ini`
oracle_user=`awk 'FS="="{if($0~/^oracle_user/) print $2}' /oper/install/rdss_config.ini`
oracle_password=`awk 'FS="="{if($0~/^oracle_password/) print $2}' /oper/install/rdss_config.ini`
oracle_service_name=`awk 'FS="="{if($0~/^oracle_service_name/) print $2}' /oper/install/rdss_config.ini`
oracle_port=`awk 'FS="="{if($0~/^oracle_port/) print $2}' /oper/install/rdss_config.ini`
#mysql_init_file_name=`awk 'FS="="{if($0~/^mysql_init_file_name/) print $2}' /oper/install/rdss_config.ini`
#redis_init_file_name=`awk 'FS="="{if($0~/^redis_init_file_name/) print $2}' /oper/install/rdss_config.ini`
#oracle_init_file_name=`awk 'FS="="{if($0~/^oracle_init_file_name/) print $2}' /oper/install/rdss_config.ini`

#返回
any_key(){
	echo  ""
	echo  "-------------------------"
	echo  "命令完成，请按回车键返回"
	ts=`date +'%Y-%m-%d.%H:%M:%S'`
	echo  "$ts 命令完成，请按回车键返回">>$log
	read wait_press
	return 0
}

#启动activemq服务
start_mq(){
	#启动activemq
	if [ "`ps -ef | grep "activemq.jar start" | grep -v grep`" != "" ];then
		echo "实时数仓activemq服务已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓activemq服务已经启动，不需要启动！">>$log
	else 
		DATE=`date +%Y%m%d`
		if [ ! -d ${rds_app_log_path}/rds_mq/log ];then
			su - weblogic -c "mkdir -p ${rds_app_log_path}/rds_mq/log"
		fi
		LOGFILENAME=${rds_app_log_path}/rds_mq/log/activemq_`date +%Y%m%d`.log
		su - weblogic -c "${rds_activemq_path}/activemq start >> $LOGFILENAME &"

		sleep 5

		if [ "`ps -ef | grep "activemq.jar start" | grep -v grep`" != "" ]; then
			echo "实时数仓activemq服务 启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓activemq服务 启动成功！！！">>$log
		else
			echo "实时数仓activemq服务 启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓activemq服务 启动失败！！！">>$log
		fi
	fi
}

#停止activemq服务
stop_mq(){
	#stop activemq
	if [ "`ps -ef | grep "activemq.jar start" | grep -v grep`" != "" ];then
		#su - weblogic -c sh /weblogic/user_projects/domains/eteller_domain/bin/stopWebLogic.sh
		
		for pid in `ps -ef | grep "activemq.jar start" | grep -v grep| awk '{print $2}'`
		do
		kill -9 $pid
		done
		
		sleep 3
		if [ "`ps -ef | grep "activemq.jar start" | grep -v grep`" != "" ]; then
			echo "实时数仓activemq服务停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓activemq服务停止失败！！！">>$log
		else
			echo "实时数仓activemq服务停止成功！！！"
			s=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓activemq服务停止成功！！！">>$log
		fi
	else 
		echo "实时数仓activemq服务已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓activemq服务已经停止，不需要重复操作！！！">>$log
	fi
}

#启动activemq、Weblogic、总线应用服务
start_app(){
																								
	#启动build
	if [ "`ps -ef| grep com.platform.ecif.build.Startup | grep -v grep`" != "" ];then
		echo "实时数仓build(1/4)组件已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓build组件(1/4)服务已经启动，不需要启动！">>$log
	else 
		su - weblogic -c "echo \"cd ${rds_dwb_path}/rds_dwb/build\">>${rds_dwb_path}/rds_dwb/build/tmp.sh"
		su - weblogic -c "echo \"sh run.sh &\">>${rds_dwb_path}/rds_dwb/build/tmp.sh"
		su - weblogic -c "echo \"sh run.sh &\">>${rds_dwb_path}/rds_dwb/build/tmp.sh"
		su - weblogic -c "chmod 755 ${rds_dwb_path}/rds_dwb/build/tmp.sh"
		su - weblogic -c "sh ${rds_dwb_path}/rds_dwb/build/tmp.sh"
		su - weblogic -c "rm -rf ${rds_dwb_path}/rds_dwb/build/tmp.sh"
		
		sleep 5

		if [ "`ps -ef| grep com.platform.ecif.build.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓build组件(1/4)服务 启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓build组件(1/4)服务 启动成功！！！">>$log
		else
			echo "实时数仓build组件(1/4)服务 启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓build组件(1/4)服务 启动失败！！！">>$log
		fi
	fi
	
	#启动execute
	if [ "`ps -ef| grep com.platform.ecif.execute.Startup | grep -v grep`" != "" ];then
		echo "实时数仓execute组件(2/4)服务已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓execute组件(2/4)服务已经启动，不需要启动！">>$log
	else 
	  su - weblogic -c "echo \"cd ${rds_dwb_path}/rds_dwb/execute\">>${rds_dwb_path}/rds_dwb/execute/tmp.sh"
		su - weblogic -c "echo \"sh run.sh &\">>${rds_dwb_path}/rds_dwb/execute/tmp.sh"
		su - weblogic -c "echo \"sh run.sh &\">>${rds_dwb_path}/rds_dwb/execute/tmp.sh"
		su - weblogic -c "chmod 755 ${rds_dwb_path}/rds_dwb/execute/tmp.sh"
		su - weblogic -c "sh ${rds_dwb_path}/rds_dwb/execute/tmp.sh"
		su - weblogic -c "rm -rf ${rds_dwb_path}/rds_dwb/execute/tmp.sh"

		sleep 5

		if [ "`ps -ef| grep com.platform.ecif.execute.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓execute组件(2/4)服务 启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓execute组件(2/4)服务 启动成功！！！">>$log
		else
			echo "实时数仓execute组件(2/4)服务 启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓execute组件(2/4)服务 启动失败！！！">>$log
		fi
	fi
	
	#启动parse
	if [ "`ps -ef| grep com.platform.ecif.parse.Startup | grep -v grep`" != "" ];then
		echo "实时数仓parse(3/4)服务已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓parse(3/4)服务已经启动，不需要启动！">>$log
	else 
	  su - weblogic -c "echo \"cd ${rds_dwb_path}/rds_dwb/parse\">>${rds_dwb_path}/rds_dwb/parse/tmp.sh"	
		su - weblogic -c "echo \"sh run.sh &\">>${rds_dwb_path}/rds_dwb/parse/tmp.sh"
		su - weblogic -c "echo \"sh run.sh &\">>${rds_dwb_path}/rds_dwb/parse/tmp.sh"
		su - weblogic -c "chmod 755 ${rds_dwb_path}/rds_dwb/parse/tmp.sh"
		su - weblogic -c "sh ${rds_dwb_path}/rds_dwb/parse/tmp.sh"
		su - weblogic -c "rm -rf ${rds_dwb_path}/rds_dwb/parse/tmp.sh"

		sleep 5

		if [ "`ps -ef| grep com.platform.ecif.parse.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓parse(3/4)服务 启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓parse(3/4)服务 启动成功！！！">>$log
		else
			echo "实时数仓parse(3/4)服务 启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓parse(3/4)服务 启动失败！！！">>$log
		fi
	fi
	
	#启动weblogic#
	if [ "`ps -ef| grep weblogic.Server|grep -v grep`" != "" ];then
		echo "实时数仓weblogic(4/4)服务已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓weblogic(4/4)服务已经启动，不需要启动！">>$log
	else 
		DATE=`date +%Y%m%d`
		if [ ! -d ${rds_app_log_path}/rds_weblogic/log ];then
			su - weblogic -c "mkdir -p ${rds_app_log_path}/rds_weblogic/log"
		fi
		LOGFILENAME=${rds_app_log_path}/rds_weblogic/log/weblogic_`date +%Y%m%d`.log
		su - weblogic -c "sh ${rds_weblogic_path}/startWebLogic.sh>${LOGFILENAME} &"

		sleep 5

		if [ "`ps -ef| grep weblogic.Server|grep -v grep`" != "" ]; then
			echo "实时数仓weblogic(4/4)服务 启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓weblogic(4/4)服务 启动成功！！！">>$log
		else
			echo "实时数仓weblogic(4/4)服务 启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓weblogic(4/4)服务 启动失败！！！">>$log
		fi
	fi
	
}


#停止activemq、Weblogic、总线应用服务
stop_app(){
	
	#stop build
	if [ "`ps -ef| grep com.platform.ecif.build.Startup | grep -v grep`" != "" ];then
		
		for pid in `ps -ef | grep com.platform.ecif.build.Startup | grep -v grep| awk '{print $2}'`
		do
		kill -9 $pid
		done
		
		sleep 3
		if [ "`ps -ef | grep com.platform.ecif.build.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓build服务停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓build服务停止失败！！！">>$log
		else
			echo "实时数仓build服务停止成功！！！"
			s=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓build服务停止成功！！！">>$log
		fi
	else 
		echo "实时数仓build服务已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓build服务已经停止，不需要重复操作！！！">>$log
	fi	
	
	#stop execute
	if [ "`ps -ef| grep com.platform.ecif.execute.Startup | grep -v grep`" != "" ];then
		
		for pid in `ps -ef | grep com.platform.ecif.execute.Startup | grep -v grep| awk '{print $2}'`
		do
		kill -9 $pid
		done
		
		sleep 3
		if [ "`ps -ef | grep com.platform.ecif.execute.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓execute服务停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓execute服务停止失败！！！">>$log
		else
			echo "实时数仓execute服务停止成功！！！"
			s=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓execute服务停止成功！！！">>$log
		fi
	else 
		echo "实时数仓execute服务已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓execute服务已经停止，不需要重复操作！！！">>$log
	fi	
	
	#stop parse
	if [ "`ps -ef| grep com.platform.ecif.parse.Startup | grep -v grep`" != "" ];then
		
		for pid in `ps -ef | grep com.platform.ecif.parse.Startup | grep -v grep| awk '{print $2}'`
		do
		kill -9 $pid
		done
		
		sleep 3
		if [ "`ps -ef | grep com.platform.ecif.parse.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓parse服务停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓parse服务停止失败！！！">>$log
		else
			echo "实时数仓parse服务停止成功！！！"
			s=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓parse服务停止成功！！！">>$log
		fi
	else 
		echo "实时数仓parse服务已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓parse服务已经停止，不需要重复操作！！！">>$log
	fi	
	
	#stop weblogic
	if [ "`ps -ef| grep weblogic.Server | grep -v grep`" != "" ];then
		
		for pid in `ps -ef | grep weblogic.Server | grep -v grep| awk '{print $2}'`
		do
		kill -9 $pid
		done
		
		sleep 3
		if [ "`ps -ef | grep weblogic.Server | grep -v grep`" != "" ]; then
			echo "实时数仓weblogic服务停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓weblogic服务停止失败！！！">>$log
		else
			echo "实时数仓weblogic服务停止成功！！！"
			s=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓weblogic服务停止成功！！！">>$log
		fi
	else 
		echo "实时数仓weblogic服务已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓weblogic服务已经停止，不需要重复操作！！！">>$log
	fi					
}

#启动实时数据抽取服务
start_scheduler(){
	if [ "`ps -ef| grep com.platform.ecif.scheduler.Startup | grep -v grep`" != "" ];then
		echo "实时数仓实时数据抽取服务（scheduler）已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓实时数据抽取服务（scheduler）已经启动，不需要启动！">>$log
	else 
		su - weblogic -c "sh ${rds_dwb_path}/rds_rde/start_rde.sh"

		sleep 5

		if [ "`ps -ef| grep com.platform.ecif.scheduler.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓实时数据抽取服务（scheduler）启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓实时数据抽取服务（scheduler）启动成功！！！">>$log
		else
			echo "实时数仓实时数据抽取服务（scheduler）启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓实时数据抽取服务（scheduler）启动失败！！！">>$log
		fi
	fi
}

#停止实时数据抽取服务
stop_scheduler(){
	if [ "`ps -ef| grep com.platform.ecif.scheduler.Startup | grep -v grep`" != "" ];then
		su - weblogic -c "sh ${rds_dwb_path}/rds_rde/stop_rde.sh"

		sleep 3

		if [ "`ps -ef| grep com.platform.ecif.scheduler.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓实时数据抽取服务（scheduler）停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓实时数据抽取服务（scheduler）停止失败！！！">>$log
		else
			echo "实时数仓实时数据抽取服务（scheduler）停止成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓实时数据抽取服务（scheduler）停止成功！！！">>$log
		fi
	else 
		echo "实时数仓实时数据抽取服务（scheduler）已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓实时数据抽取服务（scheduler）已经停止，不需要重复操作！！！">>$log
	fi
}

#clean_bcoms(){
#	echo "执行缓存清理。。。"
#	ts=`date +'%Y-%m-%d.%H:%M:%S'`
#	echo "$ts 执行缓存清理。。。">>$log
#	su - weblogic -c rm -rf /weblogic/user_projects/domains/bcoms_domain/servers/AdminServer/tmp/_WL_user/bcoms
#}

#启动实时数据抽取重发服务
start_resend(){
	if [ "`ps -ef| grep com.platform.ecif.resend.Startup | grep -v grep`" != "" ];then
		echo "实时数仓实时数据抽取重发服务（resend）已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓实时数据抽取重发服务（resend）已经启动，不需要启动！">>$log
	else 
		su - weblogic -c "sh ${rds_dwb_path}/rds_rsd/start_rsd.sh"

		sleep 5

		if [ "`ps -ef| grep com.platform.ecif.resend.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓实时数据抽取重发服务（resend）启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓实时数据抽取重发服务（resend）启动成功！！！">>$log
		else
			echo "实时数仓实时数据抽取重发服务（resend）启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓实时数据抽取重发服务（resend）启动失败！！！">>$log
		fi
	fi
}

#停止实时数据抽取重发服务
stop_resend(){
	if [ "`ps -ef| grep com.platform.ecif.resend.Startup | grep -v grep`" != "" ];then
		su - weblogic -c "sh ${rds_dwb_path}/rds_rsd/stop_rsd.sh"

		sleep 3

		if [ "`ps -ef| grep com.platform.ecif.resend.Startup | grep -v grep`" != "" ]; then
			echo "实时数仓实时数据抽取重发服务（resend）停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓实时数据抽取重发服务（resend）停止失败！！！">>$log
		else
			echo "实时数仓实时数据抽取重发服务（resend）停止成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓实时数据抽取重发服务（resend）停止成功！！！">>$log
		fi
	else 
		echo "实时数仓实时数据抽取重发服务（resend）已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓实时数据抽取重发服务（resend）已经停止，不需要重复操作！！！">>$log
	fi
}

#启动实时数仓T+1数据抽取服务（hdw_to_redis）
start_hdw_to_redis(){
	if [ "`ps -ef| grep hdw_to_redis.sh | grep -v grep`" != "" ];then
		echo "实时数仓T+1数据抽取服务（hdw_to_redis）已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓T+1数据抽取服务（hdw_to_redis）已经启动，不需要启动！">>$log
	else 
		su - mysql -c "sh /mysql/dw_script/hdw_to_redis.sh &"

		sleep 5

		if [ "`ps -ef| grep hdw_to_redis.sh | grep -v grep`" != "" ]; then
			echo "实时数仓T+1数据抽取服务（hdw_to_redis）启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓T+1数据抽取服务（hdw_to_redis）启动成功！！！">>$log
		else
			echo "实时数仓T+1数据抽取服务（hdw_to_redis）启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓T+1数据抽取服务（hdw_to_redis）启动失败！！！">>$log
		fi
	fi
}

#停止实时数仓T+1数据抽取服务（hdw_to_redis）
stop_hdw_to_redis(){
	if [ "`ps -ef| grep hdw_to_redis.sh | grep -v grep`" != "" ];then
		su - mysql -c "kill -9 `ps -ef|grep hdw_to_redis.sh|awk '{if ($8 == "sh" && $8 != "grep") print $2}'`"
		sleep 3

		if [ "`ps -ef| grep hdw_to_redis.sh | grep -v grep`" != "" ]; then
			echo "实时数仓T+1数据抽取服务（hdw_to_redis）停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓T+1数据抽取服务（hdw_to_redis）停止失败！！！">>$log
		else
			echo "实时数仓T+1数据抽取服务（hdw_to_redis）停止成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓T+1数据抽取服务（hdw_to_redis）停止成功！！！">>$log
		fi
	else 
		echo "实时数仓T+1数据抽取服务（hdw_to_redis）已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓T+1数据抽取服务（hdw_to_redis）已经停止，不需要重复操作！！！">>$log
	fi
}

#启动实时数仓扫描生成异步文件服务（rds_file_share）
start_rds_file_share(){
	if [ "`ps -ef| grep rds_file_share.sh | grep -v grep`" != "" ];then
		echo "实时数仓扫描生成异步文件服务（rds_file_share）已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓扫描生成异步文件服务（rds_file_share）已经启动，不需要启动！">>$log
	else 
		su - weblogic -c "sh /weblogic/rds_app/rds_yb_query/rds_file_share.sh &"
		sleep 5

		if [ "`ps -ef| grep rds_file_share.sh | grep -v grep`" != "" ]; then
			echo "实时数仓扫描生成异步文件服务（rds_file_share）启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓扫描生成异步文件服务（rds_file_share）启动成功！！！">>$log
		else
			echo "实时数仓扫描生成异步文件服务（rds_file_share）启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓扫描生成异步文件服务（rds_file_share）启动失败！！！">>$log
		fi
	fi
}

#停止实时数仓扫描生成异步文件服务（rds_file_share）
stop_rds_file_share(){
	if [ "`ps -ef| grep rds_file_share.sh | grep -v grep`" != "" ];then
		su - weblogic -c "kill -9 `ps -ef|grep rds_file_share.sh|awk '{if ($8 == "sh" && $8 != "grep") print $2}'`"

		sleep 3

		if [ "`ps -ef| grep rds_file_share.sh | grep -v grep`" != "" ]; then
			echo "实时数仓扫描生成异步文件服务（rds_file_share）停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓扫描生成异步文件服务（rds_file_share）停止失败！！！">>$log
		else
			echo "实时数仓扫描生成异步文件服务（rds_file_share）停止成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓扫描生成异步文件服务（rds_file_share）停止成功！！！">>$log
		fi
	else 
		echo "实时数仓扫描生成异步文件服务（rds_file_share）已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓扫描生成异步文件服务（rds_file_share）已经停止，不需要重复操作！！！">>$log
	fi
}

#启动实时数仓redis数据归档服务（redis_bk_del）
start_redis_bk_del(){
	if [ "`ps -ef| grep redis_bk_del.sh | grep -v grep`" != "" ];then
		echo "实时数仓redis数据归档服务（redis_bk_del）已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓redis数据归档服务（redis_bk_del）已经启动，不需要启动！">>$log
	else 
		su - redis -c "nohup sh /redis/redis_data_backup/redis_bk_del.sh 2>&1>/redis/redis_data_backup/redis_bk_del.log &"

		sleep 5

		if [ "`ps -ef| grep redis_bk_del.sh | grep -v grep`" != "" ]; then
			echo "实时数仓redis数据归档服务（redis_bk_del）启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓redis数据归档服务（redis_bk_del）启动成功！！！">>$log
		else
			echo "实时数仓redis数据归档服务（redis_bk_del）启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓redis数据归档服务（redis_bk_del）启动失败！！！">>$log
		fi
	fi
}

#停止实时数仓redis数据归档服务（redis_bk_del）
stop_redis_bk_del(){
	if [ "`ps -ef| grep redis_bk_del.sh | grep -v grep`" != "" ];then
		su - redis -c "kill -9 `ps -ef|grep redis_bk_del.sh|awk '{if ($8 == "sh" && $8 != "grep") print $2}'`"
		sleep 3

		if [ "`ps -ef| grep redis_bk_del.sh | grep -v grep`" != "" ]; then
			echo "实时数仓redis数据归档服务（redis_bk_del）停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓redis数据归档服务（redis_bk_del）停止失败！！！">>$log
		else
			echo "实时数仓redis数据归档服务（redis_bk_del）停止成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓redis数据归档服务（redis_bk_del）停止成功！！！">>$log
		fi
	else 
		echo "实时数仓redis数据归档服务（redis_bk_del）已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓redis数据归档服务（redis_bk_del）已经停止，不需要重复操作！！！">>$log
	fi
}

#启动实时数仓总线应用日志备份清理服务（rds_log_bak_daily）
start_rds_log_bak_daily(){
	if [ "`ps -ef| grep rds_log_bak_daily.sh | grep -v grep`" != "" ];then
		echo "实时数仓总线应用日志备份清理服务（rds_log_bak_daily）已经启动，不需要启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓总线应用日志备份清理服务（rds_log_bak_daily）已经启动，不需要启动！">>$log
	else 
		su - weblogic -c "nohup sh /weblogic/rds_app/script/rds_log_bak_daily.sh 2>&1>/weblogic/rds_app/script/rds_log_bak_daily.log &"

		sleep 5

		if [ "`ps -ef| grep rds_log_bak_daily.sh | grep -v grep`" != "" ]; then
			echo "实时数仓总线应用日志备份清理服务（rds_log_bak_daily）启动成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓总线应用日志备份清理服务（rds_log_bak_daily）启动成功！！！">>$log
		else
			echo "实时数仓总线应用日志备份清理服务（rds_log_bak_daily）启动失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓总线应用日志备份清理服务（rds_log_bak_daily）启动失败！！！">>$log
		fi
	fi
}

#停止实时数仓总线应用日志备份清理服务（rds_log_bak_daily）
stop_rds_log_bak_daily(){
	if [ "`ps -ef| grep rds_log_bak_daily.sh | grep -v grep`" != "" ];then
		su - weblogic -c "kill -9 `ps -ef|grep rds_log_bak_daily.sh|awk '{if ($8 == "sh" && $8 != "grep") print $2}'`"
		sleep 3

		if [ "`ps -ef| grep rds_log_bak_daily.sh | grep -v grep`" != "" ]; then
			echo "实时数仓总线应用日志备份清理服务（rds_log_bak_daily）停止失败！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓总线应用日志备份清理服务（rds_log_bak_daily）停止失败！！！">>$log
		else
			echo "实时数仓总线应用日志备份清理服务（rds_log_bak_daily）停止成功！！！"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓总线应用日志备份清理服务（rds_log_bak_daily）停止成功！！！">>$log
		fi
	else 
		echo "实时数仓总线应用日志备份清理服务（rds_log_bak_daily）已经停止，不需要重复操作！！！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓总线应用日志备份清理服务（rds_log_bak_daily）已经停止，不需要重复操作！！！">>$log
	fi
}

#端口检查
portCheck(){
	port_3306=3306
	num_3306=`netstat -an | grep "$port_3306" | awk '$1=="tcp" && $NF=="LISTEN" {print $0}' | wc -l`
	if [ $num_3306 -ge 1 ]
		then
		echo "实时数仓mysql服务端口号$port_3306 监听已启动"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓mysql服务端口号$port_3306 监听已启动">>$log
	else
		echo "实时数仓mysql服务端口号$port_3306 监听已停止"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓mysql服务端口号$port_3306 监听已停止">>$log
	fi
	
	port_6379=6379
	num_6379=`netstat -an | grep "$port_6379" | awk '$1=="tcp" && $NF=="LISTEN" {print $0}' | wc -l`
	if [ $num_6379 -ge 1 ]
		then
		echo "实时数仓redis服务端口号$port_6379 监听已启动"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓redis服务端口号$port_6379 监听已启动">>$log
	else
		echo "实时数仓redis服务端口号$port_6379 监听已停止"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓redis服务端口号$port_6379 监听已停止">>$log
	fi

	any_key;
}

#进程检查progressCheck
progressCheck(){
	if [ "`ps -ef | grep "activemq.jar start" | grep -v grep`" != "" ]
		then 
		echo "实时数仓activemq服务              已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓activemq服务已启动！">>$log
	else
		echo "实时数仓activemq服务              已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓activemq服务已停止！">>$log
	fi

	if [ "`ps -ef| grep com.platform.ecif.build.Startup | grep -v grep`" != "" ]
		then 
		echo "实时数仓build服务                 已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓build服务已启动！">>$log
	else
		echo "实时数仓build服务                 已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓build服务已停止！">>$log
	fi

	if [ "`ps -ef| grep com.platform.ecif.execute.Startup | grep -v grep`" != "" ]
		then 
		echo "实时数仓execute服务               已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓execute服务已启动！">>$log
	else
		echo "实时数仓execute服务               已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓execute服务已停止！">>$log
	fi

	if [ "`ps -ef| grep com.platform.ecif.parse.Startup | grep -v grep`" != "" ]
		then 
		echo "实时数仓parse服务                 已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓parse服务已启动！">>$log
	else
		echo "实时数仓parse服务                 已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓parse服务已停止！">>$log
	fi
	
	if [ "`ps -ef| grep weblogic.Server | grep -v grep`" != "" ]
		then 
		echo "实时数仓weblogic服务              已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓weblogic服务已启动！">>$log
	else
		echo "实时数仓weblogic服务              已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓weblogic服务已停止！">>$log
	fi	
	
	if [ "`ps -ef| grep com.platform.ecif.scheduler.Startup | grep -v grep`" != "" ]
		then 
		echo "实时数仓scheduler服务             已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓scheduler服务已启动！">>$log
	else
		echo "实时数仓scheduler服务             已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓scheduler服务已停止！">>$log
	fi		
	
	if [ "`ps -ef| grep com.platform.ecif.resend.Startup | grep -v grep`" != "" ]
		then 
		echo "实时数仓resend服务                已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓resend服务已启动！">>$log
	else
		echo "实时数仓resend服务                已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓resend服务已停止！">>$log
	fi	
	
	if [ "`ps -ef| grep mysqld | grep -v grep`" != "" ]
		then 
		echo "实时数仓mysql服务                 已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓mysql服务已启动！">>$log
	else
		echo "实时数仓mysql服务                 已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓mysql服务已停止！">>$log
	fi	
	
	if [ "`ps -ef| grep redis-server | grep -v grep`" != "" ]
		then 
		echo "实时数仓redis服务                 已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓redis服务已启动！">>$log
	else
		echo "实时数仓redis服务                 已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓redis服务已停止！">>$log
	fi	
	
	if [ "`ps -ef| grep redis_bk_del.sh | grep -v grep`" != "" ]
		then 
		echo "实时数仓redis归档服务             已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓redis归档服务已启动！">>$log
	else
		echo "实时数仓redis归档服务             已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓redis归档服务已停止！">>$log
	fi
	
	if [ "`ps -ef| grep hdw_to_redis.sh | grep -v grep`" != "" ]
		then 
		echo "实时数仓T+1数据抽取服务           已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓T+1数据抽取服务已启动！">>$log
	else
		echo "实时数仓T+1数据抽取服务           已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓T+1数据抽取服务已停止！">>$log
	fi
	
	if [ "`ps -ef| grep rds_file_share.sh | grep -v grep`" != "" ]
		then 
		echo "实时数仓扫描生成异步文件服务      已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓扫描生成异步文件服务已启动！">>$log
	else
		echo "实时数仓扫描生成异步文件服务      已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓扫描生成异步文件服务已停止！">>$log
	fi		
	
	if [ "`ps -ef| grep rds_log_bak_daily.sh | grep -v grep`" != "" ]
		then 
		echo "实时数仓总线应用日志备份清理服务  已启动！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓总线应用日志备份清理服务已启动！">>$log
	else
		echo "实时数仓总线应用日志备份清理服务  已停止！"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo "$ts 实时数仓总线应用日志备份清理服务已停止！">>$log
	fi		

	any_key;
}

#1.1 & 2.1服务检查serverCheck
serverCheck(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------"
	echo "|            服务检查                  |"
	echo "|--------------------------------------|"
	echo "| 1.进程检查                           |"
	echo "| 2.端口检查                           |"
	echo "|                                      |"
	echo "| 0.返回上级菜单                       |"
	echo "---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)progressCheck;;
		2)portCheck;;
		esac
done
}

#1无密码模式noPasswordModel
noPasswordModel(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------"
	echo "|       应用系统维护菜单               |"
	echo "|--------------------------------------|"
	echo "|        1.服务检查                    |"
	echo "|        0.返回上级菜单                |"
	echo "---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)serverCheck;;
		*)continue;;
	esac
done 
}

#服务启停
serveroper(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------------------------------"
	echo "|                            服务启停                         |"
	echo "|-------------------------------------------------------------|"
	echo "|    应用服务器 11.1.3.56、11.1.3.57 启停服务：               |"
	echo "|                                                             |"
	echo "|  1.启动实时数仓activemq服务                                 |"
	echo "|  2.停止实时数仓activemq服务                                 |"
	echo "|  3.启动实时数仓Weblogic、总线应用服务                       |"
	echo "|  4.停止实时数仓Weblogic、总线应用服务                       |"
	echo "|  5.启动实时数仓实时数据抽取服务（scheduler）                |"
	echo "|  6.停止实时数仓实时数据抽取服务（scheduler）                |"
	echo "|  7.启动实时数仓实时数据抽取重发服务（resend）               |"
	echo "|  8.停止实时数仓实时数据抽取重发服务（resend）               |"
	echo "|  9.启动实时数仓扫描生成异步文件服务（rds_file_share）       |"
	echo "| 10.停止实时数仓扫描生成异步文件服务（rds_file_share）       |"
	echo "| 11.启动实时数仓总线应用日志备份清理服务（rds_log_bak_daily）|"
	echo "| 12.停止实时数仓总线应用日志备份清理服务（rds_log_bak_daily）|"
	echo "|-------------------------------------------------------------|"
	echo "|    Mysql服务器 11.1.3.58、11.1.3.59 启停服务：              |"
	echo "|                                                             |"
	echo "| 13.启动实时数仓T+1数据抽取服务（hdw_to_redis）              |"
	echo "| 14.停止实时数仓T+1数据抽取服务（hdw_to_redis）              |"
	echo "| 15.启动实时数仓redis数据归档服务（redis_bk_del）            |"
	echo "| 16.停止实时数仓redis数据归档服务（redis_bk_del）            |"
#	echo "| 17.清除流程银行weblogic应用缓存（bcoms_domain）     |"
	echo "|-------------------------------------------------------------|"
	echo "|  0.返回上级菜单                                             |"
	echo "---------------------------------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)echo "启动实时数仓activemq服务 ？ (y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 启动实时数仓activemq服务 ？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "启动实时数仓activemq服务开始"	
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 启动实时数仓activemq服务开始">>$log
				start_mq
			fi
			any_key;;
		2)echo "停止实时数仓activemq服务？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓activemq服务？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				 echo "停止实时数仓activemq服务开始" 
				 ts=`date +'%Y-%m-%d.%H:%M:%S'`
				 echo "$ts 停止实时数仓activemq服务开始">>$log
				 stop_mq
			fi
			any_key;;		
		3)echo "启动实时数仓Weblogic、总线应用服务 ？ (y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 启动实时数仓Weblogic、总线应用服务 ？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "启动实时数仓Weblogic、总线应用服务开始"	
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 启动实时数仓Weblogic、总线应用服务开始">>$log
				start_app
			fi
			any_key;;
		4)echo "停止实时数仓Weblogic、总线应用服务？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 实时数仓Weblogic、总线应用服务？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				 echo "停止实时数仓Weblogic、总线应用服务开始" 
				 ts=`date +'%Y-%m-%d.%H:%M:%S'`
				 echo "$ts 停止实时数仓Weblogic、总线应用服务开始">>$log
				 stop_app
			fi
			any_key;;
		5)echo "是否启动实时数仓实时数据抽取服务（scheduler）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否启动实时数仓实时数据抽取服务（scheduler）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "启动实时数仓实时数据抽取服务（scheduler）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 启动实时数仓实时数据抽取服务（scheduler）开始">>$log
				start_scheduler
			fi
			any_key;;
		6)echo "是否停止实时数仓实时数据抽取服务（scheduler）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否停止实时数仓实时数据抽取服务（scheduler）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "停止实时数仓实时数据抽取服务（scheduler）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 停止实时数仓实时数据抽取服务（scheduler）开始">>$log
				stop_scheduler
			fi
			any_key;;
		7)echo "是否启动实时数仓实时数据抽取重发服务（resend）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否启动实时数仓实时数据抽取重发服务（resend）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "启动实时数仓实时数据抽取重发服务（resend）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 启动实时数仓实时数据抽取重发服务（resend）开始">>$log
				start_resend
			fi
			any_key;;
		8)echo "是否停止实时数仓实时数据抽取重发服务（resend）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否停止实时数仓实时数据抽取重发服务（resend）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "停止实时数仓实时数据抽取重发服务（resend）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 停止实时数仓实时数据抽取重发服务（resend）开始">>$log
				stop_resend
			fi
			any_key;;
		9)echo "是否启动实时数仓扫描生成异步文件服务（rds_file_share）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否启动实时数仓扫描生成异步文件服务（rds_file_share）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "启动实时数仓扫描生成异步文件服务（rds_file_share）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 启动实时数仓扫描生成异步文件服务（rds_file_share）开始">>$log
				start_rds_file_share
			fi
			any_key;;
		10)echo "是否停止实时数仓扫描生成异步文件服务（rds_file_share）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否停止实时数仓扫描生成异步文件服务（rds_file_share）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "停止实时数仓扫描生成异步文件服务（rds_file_share）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 停止实时数仓扫描生成异步文件服务（rds_file_share）开始">>$log
				stop_rds_file_share
			fi
			any_key;;
		11)echo "是否启动实时数仓总线应用日志备份清理服务（rds_log_bak_daily）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否启动实时数仓总线应用日志备份清理服务（rds_log_bak_daily）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "启动实时数仓总线应用日志备份清理服务（rds_log_bak_daily）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 启动实时数仓总线应用日志备份清理服务（rds_log_bak_daily）开始">>$log
				start_rds_log_bak_daily
			fi
			any_key;;
		12)echo "是否停止实时数仓总线应用日志备份清理服务（rds_log_bak_daily）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否停止实时数仓总线应用日志备份清理服务（rds_log_bak_daily）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "停止实时数仓总线应用日志备份清理服务（rds_log_bak_daily）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 停止实时数仓总线应用日志备份清理服务（rds_log_bak_daily）开始">>$log
				stop_rds_log_bak_daily
			fi			
			any_key;;
		13)echo "是否启动实时数仓T+1数据抽取服务（hdw_to_redis）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否启动实时数仓T+1数据抽取服务（hdw_to_redis）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "启动实时数仓T+1数据抽取服务（hdw_to_redis）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 启动实时数仓T+1数据抽取服务（hdw_to_redis）开始">>$log
				start_hdw_to_redis
			fi
			any_key;;
		14)echo "是否停止实时数仓T+1数据抽取服务（hdw_to_redis）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否停止实时数仓T+1数据抽取服务（hdw_to_redis）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "停止实时数仓T+1数据抽取服务（hdw_to_redis）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 停止实时数仓T+1数据抽取服务（hdw_to_redis）开始">>$log
				stop_hdw_to_redis
			fi
			any_key;;
		15)echo "是否启动实时数仓redis数据归档服务（redis_bk_del）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否启动实时数仓redis数据归档服务（redis_bk_del）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "启动实时数仓redis数据归档服务（redis_bk_del）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 启动实时数仓redis数据归档服务（redis_bk_del）开始">>$log
				start_redis_bk_del
			fi
			any_key;;
		16)echo "是否停止实时数仓redis数据归档服务（redis_bk_del）？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否停止实时数仓redis数据归档服务（redis_bk_del）？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "停止实时数仓redis数据归档服务（redis_bk_del）开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 停止实时数仓redis数据归档服务（redis_bk_del）开始">>$log
				stop_redis_bk_del
			fi			
			any_key;;
#		17)echo "是否清除流程银行weblogic应用缓存（bcoms_domain）？(y/n)"
#			ts=`date +'%Y-%m-%d.%H:%M:%S'`
#			echo "$ts 是否清除流程银行weblogic应用缓存（bcoms_domain）？(y/n)">>$log
#			read yn
#			ts=`date +'%Y-%m-%d.%H:%M:%S'`
#			echo "$ts $yn">>$log
#			if [ "X$yn" != "Xy" ]
#				then
#					continue
#			else
#				echo "清除流程银行weblogic应用缓存（bcoms_domain）开始"
#				ts=`date +'%Y-%m-%d.%H:%M:%S'`
#				echo "$ts 清除流程银行weblogic应用缓存（bcoms_domain）开始">>$log
#				clean_bcoms
#			fi
#			any_key;;			
		*)continue;;
	esac
done
}

#数据库备份
backupSql(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "-----------------------------------"
	echo "|          备份数据库部分          |"
	echo "|----------------------------------|"
	echo "| 1.备份mysql数据库                |"
	echo "| 2.备份redis数据库                |"
	echo "|                                  |"
	echo "| 0.返回上级菜单                   |"
	echo "-----------------------------------"
	echo -e "  选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)echo "是否备份mysql数据库？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否备份mysql数据库？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "备份mysql数据库开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 备份mysql数据库开始">>$log
				bakMysql
			fi
			any_key;;
		2)echo "是否备份redis数据库？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否备份redis数据库？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "备份redis数据库开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 备份redis数据库开始">>$log
				bakRedis
			fi
			any_key;;
		*)continue;
	esac
done
}

#备份应用部分
backupApp(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------"
	echo "|              备份应用部分            |"
	echo "|--------------------------------------|"
	echo "| 1.备份应用                           |"
	echo "|                                      |"
	echo "| 0.返回上级菜单                       |"
	echo "---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)echo "是否备份应用？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否备份应用？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "备份应用开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 备份应用开始">>$log
				bakApp
			fi
			any_key;;
		*)continue;;
	esac
done
}

#部署应用部分
installApp(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------"
	echo "|             部署应用部分             |"
	echo "|--------------------------------------|"
	echo "| 1.部署RDSS应用                       |"
	echo "|                                      |"
	echo "| 0.返回上级菜单                       |"
	echo "---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)echo "是否部署RDSS应用？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否部署RDSS应用？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "部署RDSS应用开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 部署RDSS应用开始">>$log
				installRdssApp
			fi
			any_key;;
		*)continue;;
	esac
done
}

#部署数据库部分
installSql(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------"
	echo "|            部署数据库部分            |"
	echo "|--------------------------------------|"
	echo "| 1.部署mysql数据库脚本                |"
	echo "| 2.部署redis数据库脚本                |"
	echo "| 3.部署oracle数据库脚本               |"
	echo "|                                      |"
	echo "| 0.返回上级菜单                       |"
	echo "---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)echo "是否部署mysql数据库脚本？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否部署mysql数据库脚本？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "部署mysql数据库脚本开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 部署mysql数据库脚本开始">>$log
				installMysql
			fi
			any_key;;
		2)echo "是否部署redis数据库脚本？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否部署redis数据库脚本？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "部署redis数据库脚本开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 部署redis数据库脚本开始">>$log
				installRedis
			fi
			any_key;;
		3)echo "是否部署oracle数据库脚本？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否部署oracle数据库脚本？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "部署oracle数据库脚本开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 部署oracle数据库脚本开始">>$log
				installOracle
			fi
			any_key;;			
		*)continue;;
	esac
done
}

#回滚数据库部分
rollbackSql(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------"
	echo "|            回滚数据库部分            |"	
	echo "|--------------------------------------|"
	echo "| 1.回滚mysql数据库                    |"
	echo "| 2.回滚redis数据库                    |"
	echo "|                                      |"
	echo "| 0.返回上级菜单                       |"
	echo "---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)echo "是否回滚mysql数据库？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否回滚mysql数据库？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log			
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "回滚mysql数据库开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 回滚mysql数据库开始">>$log
				rollbackMysql
			fi
			any_key;;
		2)echo "是否回滚redis数据库？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否回滚redis数据库？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "回滚redis数据库开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 回滚redis数据库开始">>$log
				rollbackRedis
			fi
			any_key;;
		*)continue;;
	esac
done
}

#回滚应用部分
rollbackApp(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------"
	echo "|              回滚应用部分            |"	
	echo "|--------------------------------------|"
	echo "| 1.回滚RDSS应用                       |"
	echo "|                                      |"
	echo "| 0.返回上级菜单                       |"
	echo "---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)echo "是否回滚RDSS应用？(y/n)"
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts 是否回滚RDSS应用？(y/n)">>$log
			read yn
			ts=`date +'%Y-%m-%d.%H:%M:%S'`
			echo "$ts $yn">>$log			
			if [ "X$yn" != "Xy" ]
				then
					continue
			else
				echo "回滚RDSS应用开始"
				ts=`date +'%Y-%m-%d.%H:%M:%S'`
				echo "$ts 回滚RDSS应用开始">>$log
				rollbackRdssApp
			fi
			any_key;;
		*)continue;;
	esac
done
}

#投产变更
prdChange(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------"
	echo "|              投产变更                |"
	echo "|--------------------------------------|"
	echo "| 1.备份数据库部分                     |"
	echo "| 2.备份应用部分                       |"
	echo "| 3.部署数据库部分                     |"	
	echo "| 4.部署应用部分                       |"
	echo "| 5.回滚数据库部分                     |"	
	echo "| 6.回滚应用部分                       |"	
	echo "|                                      |"
	echo "| 0.返回上级菜单                       |"
	echo "---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)backupSql;;
		2)backupApp;;
		3)installSql;;
		4)installApp;;		
		5)rollbackSql;;		
		6)rollbackApp;;
		*)continue;;
	esac
done
}

#密码模式菜单
passwordModelMenu(){
while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT
	echo ""
	echo "---------------------------------------"
	echo "|       应用系统维护菜单               |"
	echo "|--------------------------------------|"
	echo "|        1.服务检查                    |"
	echo "|        2.服务启停                    |"
	echo "|        3.投产变更                    |"
	echo "|                                      |"
	echo "|        0.返回上级菜单                |"
	echo "---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)return;;
		1)serverCheck;;
		2)serveroper;;
		3)prdChange;;
		*)continue;;
	esac
done
}

#密码模式
passwordModel(){
	trap '' INT
	echo -e "请输入密码：\c"
	stty -echo
	read passwd
	stty echo
	if [ "$passwd"x = "oper"x ]
		then
		passwordModelMenu;
	else
		echo -e "\n密码输入错误"
		ts=`date +'%Y-%m-%d.%H:%M:%S'`
		echo -e "$ts \n密码输入错误">>$log
		any_key;
	fi
}

#0主函数,入口界面

#定义脚本操作日志
curdate=`date +%Y%m%d`
su - weblogic -c mkdir -p /oper/log
log="/oper/log/menu$curdate.log"
if [ ! -f $log ]; then
  >>$log
  chmod 777 $log
else
	cat null>>$log
fi
installMysqlDblog="/oper/log/MysqlDb$curdate.log"
if [ ! -f $installMysqlDblog ]; then
	  >>$installMysqlDblog
	  chmod 777 $installMysqlDblog
else
		cat null>>$installMysqlDblog
fi

installRedisDblog="/oper/log/RedisDb$curdate.log"
if [ ! -f $installRedisDblog ]; then
	  >>$installRedisDblog
	  chmod 777 $installRedisDblog
else
		cat null>>$installRedisDblog
fi

installOracleDblog="/oper/log/OracleDb$curdate.log"
if [ ! -f $installOracleDblog ]; then
	  >>$installOracleDblog
	  chmod 777 $installOracleDblog
else
		cat null>>$installOracleDblog
fi

#installCostDblog="/oper/log/CostDb$curdate.log"
#if [ ! -f $installCostDblog ]; then
#	  >>$installCostDblog
#	  chmod 777 $installCostDblog
#else
#		cat null>>$installCostDblog
#fi
#
#installInsopDblog="/oper/log/InsopDb$curdate.log"
#if [ ! -f $installInsopDblog ]; then
#	  >>$installInsopDblog
#	  chmod 777 $installInsopDblog
#else
#		cat null>>$installInsopDblog
#fi
#
#bakEtellerDblog="/oper/log/bakEteller$curdate.log"
#if [ ! -f $bakEtellerDblog ]; then
#	 	>>$bakEtellerDblog
#	  chmod 777 $bakEtellerDblog
#else
#		cat null>>$bakEtellerDblog
#fi
#
#bakBcomsDblog="/oper/log/bakBcoms$curdate.log"
#if [ ! -f $bakBcomsDblog ]; then
#	  >>$bakBcomsDblog
#	  chmod 777 $bakBcomsDblog
#else
#		cat null>>$bakBcomsDblog
#fi
#
#bakCostDblog="/oper/log/bakCost$curdate.log"
#if [ ! -f $bakCostDblog ]; then
#	  >>$bakCostDblog
#	  chmod 777 $bakCostDblog
#else
#		cat null>>$bakCostDblog
#fi
#
#bakInsopDblog="/oper/log/bakInsop$curdate.log"
#if [ ! -f $bakInsopDblog ]; then
#	  >>$bakInsopDblog
#	  chmod 777 $bakInsopDblog
#else
#		cat null>>$bakInsopDblog
#fi

ts=`date +'%Y-%m-%d.%H:%M:%S'`
echo "$ts 进入菜单操作" >>$log

while true
do
	clear
	#屏蔽Ctrl+C组合键
	trap '' INT 
  echo  ""   
  echo  "           实时数据服务系统上线部署       "
	echo  ""  
  echo  "      RDSS --  应用服务器 11.1.3.56/57"
  echo  "      RDSS -- Mysql服务器 11.1.3.58/59"  
  echo  "      RDSS -- Redis服务器 11.1.3.60/61"   
	echo  ""	  
	echo  "   ---------------------------------------"
	echo  "   |       应用系统维护菜单               |"
	echo  "   |--------------------------------------|"
	echo  "   |        1.无密码模式                  |"
	echo  "   |        2.密码模式                    |"
	echo  "   |                                      |"
	echo  "   |        0.退出菜单                    |"
	echo  "   ---------------------------------------"
	echo -e "         选菜单:\c"
	read choice
	case $choice in
		0)echo ""
			echo "退出功能已被禁用"
			any_key;;
		1)noPasswordModel;;
		2)passwordModel;;
#		youbest)exit;;  
		*)continue;;
	esac
	ts=`date +'%Y-%m-%d.%H:%M:%S'`
	echo "$ts 退出菜单操作" >>$log
done