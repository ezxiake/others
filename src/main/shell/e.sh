#!/bin/bash
#--------------------------------------------------------------------
# Fuction
# Version: 1.0
# Created: ****
# Created date:2017/11/14
# Modify history:
#--------------------------------------------------------------------

trap '' 2 3 15 20

### defined variable ###

declare -A d_zone_vpc_subnet_oregon
d_zone_vpc_subnet_oregon+=([us-west-2a]="subnet-24a89d52")
d_zone_vpc_subnet_oregon+=([us-west-2b]="subnet-75ffec11")

declare -A d_zone_vpc_subnet_singapore
d_zone_vpc_subnet_singapore+=([ap-southeast-1a]="subnet-a51384c1")
d_zone_vpc_subnet_singapore+=([ap-southeast-1b]="subnet-a525a2d3")

declare -A d_region_oregon
d_region_oregon=([region]="us-west-2" [vpc_id]="vpc-8ffb0ce8" [image]="ami-0d10b1979afc575ba")

declare -A d_region_singapore
d_region_singapore=([region]="ap-southeast-1" [vpc_id]="vpc-0fa4756b" [image]="ami-08be42f18e932d3fb")

# instance type
l_general_purpose=("t2.nano" "t2.micro" "t2.small" "t2.medium" "t2.large" "t2.xlarge" "t2.2xlarge" "t3.nano" "t3.micro" "t3.small" "t3.medium" "t3.large" "t3.xlarge" "t3.2xlarge" "m4.large" "m4.xlarge" "m4.2xlarge" "m4.4xlarge" "m4.10xlarge" "m4.16xlarge" "m5.large" "m5.xlarge" "m5.2xlarge" "m5.4xlarge" "m5.12xlarge" "m5.24xlarge" "m5d.large" "m5d.xlarge" "m5d.2xlarge" "m5d.4xlarge" "m5d.12xlarge" "m5d.24xlarge")
l_compute_optimized=("c4.large" "c4.xlarge" "c4.2xlarge" "c4.4xlarge" "c4.8xlarge" "c5.large" "c5.xlarge" "c5.2xlarge" "c5.4xlarge" "c5.9xlarge" "c5.18xlarge" "c5d.xlarge" "c5d.2xlarge" "c5d.4xlarge" "c5d.9xlarge" "c5d.18xlarge")
l_memory_optimized=("r4.large" "r4.xlarge" "r4.2xlarge" "r4.4xlarge" "r4.8xlarge" "r4.16xlarge" "r5.large" "r5.xlarge" "r5.2xlarge" "r5.4xlarge" "r5.12xlarge" "r5.24xlarge" "r5d.large" "r5d.xlarge" "r5d.2xlarge" "r5d.4xlarge" "r5d.12xlarge" "r5d.24xlarge" "x1.16xlarge" "x1.32xlarge" "x1e.xlarge" "x1e.2xlarge" "x1e.4xlarge" "x1e.8xlarge" "x1e.16xlarge" "x1e.32xlarge" "z1d.large" "z1d.xlarge" "z1d.2xlarge" "z1d.3xlarge" "z1d.6xlarge" "z1d.12xlarge")
l_storage_optimized=("d2.xlarge" "d2.2xlarge" "d2.4xlarge" "d2.8xlarge" "h1.2xlarge" "h1.4xlarge" "h1.8xlarge" "h1.16xlarge" "i3.large" "i3.xlarge" "i3.2xlarge" "i3.4xlarge" "i3.8xlarge" "i3.16xlarge")
l_accelerated_computing=("f1.2xlarge" "f1.4xlarge" "f1.16xlarge" "g3s.xlarge" "g3.4xlarge" "g3.8xlarge" "g3.16xlarge" "p2.xlarge" "p2.8xlarge" "p2.16xlarge" "p3.2xlarge" "p3.8xlarge" "p3.16xlarge")
l_bare_metal=("i3.metal" "u-6tb1.metal" "u-9tb1.metal" "u-12tb1.metal")

declare -A d_disk_info_mapping
d_disk_info_mapping=([1]="b" [2]="c" [3]="d" [4]="e" [5]="f" [6]="g" [7]="h" [8]="i" [9]="j")

declare -A d_disk_size_mapping
d_disk_size_mapping=([1]="10" [2]="20" [3]="30" [4]="40" [5]="50" [6]="60" [7]="70" [8]="80" [9]="90")

declare -A d_disk_path_mapping
d_disk_path_mapping=([1]="/data1" [2]="/data2" [3]="/data3" [4]="/data4" [5]="/data5" [6]="/data6" [7]="/data7" [8]="/data8" [9]="/data9")

v_create_aws_instance_cluster_name=
v_create_aws_instance_cluster_security_group_name=
v_create_aws_instance_region=
v_create_aws_instance_vpc_id=
v_create_aws_instance_image=
v_create_aws_instance_zone=
v_create_aws_instance_vpc_subnet=
v_create_aws_instance_type=
v_create_aws_instance_count=
v_create_aws_instance_key_name=
v_create_aws_instance_root_disk_size=
v_create_aws_instance_data_disk_count=


### functions ###
any_key(){
	echo  ""
	echo  "-----------------------------------------------"
	echo  -e "\033[42;37;5m Completed, press Enter to continue \033[0m"
	read wait_press
	return 0
}

input_error_key(){ 
	echo  ""
	echo  "-----------------------------------------------"
	echo  -e "\033[44;37;5m Invalid choice, re-enter after press Enter \033[0m"
	read wait_press
	return 0
}

cannot_be_empty(){ 
	echo  ""
	echo  "-----------------------------------------------"
	echo  -e "\033[44;37;5m This item cannot be empty, re-enter after press Enter \033[0m"
	read wait_press
	return 0
}

not_a_valid_number(){ 
	echo  ""
	echo  "-----------------------------------------------"
	echo  -e "\033[44;37;5m This item is not a valid number, re-enter after press Enter \033[0m"
	read wait_press
	return 0
}

confirm_entry(){
	fieldName=$1
	fieldValue=$2
	while true
	do
		echo  ""
		echo  "-----------------------------------------------"
		echo  -e "\033[47;30m ${fieldName} is ${fieldValue} \033[0m"
		read -p "Confirm input y, re-enter input n:" confirm_entry_choice
		case $confirm_entry_choice in        
		 [Yy]) return 0 ;;             
		 [Nn]) return 1 ;;
		    *) input_error_key ;;
		esac
	done
}
 
xxxxxxxx() {
	while true
	do
		clear
		echo -e "\n-----------------Create the new AWS instance or instances-----------------"  
		echo -e " cluster name : ${v_create_aws_instance_cluster_name}"
		echo -e " cluster security group name : ${v_create_aws_instance_cluster_security_group_name}"
		echo -e " region : ${v_create_aws_instance_region}"
		echo -e " vpc_id : "
		echo -e " image : "
		echo -e " zone : "
		echo -e " vpc_subnet : "
		echo -e " aws_cluster_type : "
		echo -e " aws_cluster_count : "
		echo -e " aws_key_name : "
		echo -e " root disk size(GB) : "
		echo -e " data disk count : "
		echo -e ""
		echo -e " (r) Return"
		echo -e " ----------------------------------"  
		read -p "Please input your cluster name:" create_aws_instance_menu_choice
		case $create_aws_instance_menu_choice in        
		 [Rr]) return ;;             
		    *)
		    	confirm_entry 'cluster name' $create_aws_instance_menu_choice
		    	if [ $? -eq 0 ]
		    		then
		    		v_create_aws_instance_cluster_name=$create_aws_instance_menu_choice
		    		v_create_aws_instance_cluster_security_group_name=${v_create_aws_instance_cluster_name}_group
		    		break
		    	else
		    		continue
		    	fi
		    	;;
		esac
	done
}

debugging() {

	### debugging
	echo -e ""
	echo -e "cluster name : ${v_create_aws_instance_cluster_name}"
	echo -e "security group : ${v_create_aws_instance_cluster_security_group_name}"
	echo -e "region : ${v_create_aws_instance_region}"
	echo -e "vpc id : ${v_create_aws_instance_vpc_id}"
	echo -e "image : ${v_create_aws_instance_image}"
	echo -e "zone : ${v_create_aws_instance_zone}"
	echo -e "vpc subnet ：${v_create_aws_instance_vpc_subnet}"
	echo -e "instance type : ${v_create_aws_instance_type}"
	echo -e "instance count : ${v_create_aws_instance_count}"
	echo -e "key name : ${v_create_aws_instance_key_name}"
	echo -e "root disk size : ${v_create_aws_instance_root_disk_size}"
	echo -e "data disk count : ${v_create_aws_instance_data_disk_count}"
	echo -e ""
	echo -e " (r) Return"
	echo -e " (x) Exit"
	echo -e "-------------------------------------------------------------------------------"
	#########################################################################################
	echo "---">./create_aws_instance_by_script.yml
	echo "cluster_node_price:">>./create_aws_instance_by_script.yml
	echo "spot_wait_timeout: 900">>./create_aws_instance_by_script.yml
	echo "assign_public_ip: yes">>./create_aws_instance_by_script.yml
	echo "placement_group:">>./create_aws_instance_by_script.yml
	echo "cluster_security_group: ${v_create_aws_instance_cluster_security_group_name}">>./create_aws_instance_by_script.yml
	echo "region: ${v_create_aws_instance_region}">>./create_aws_instance_by_script.yml
	echo "cluster_name: ${v_create_aws_instance_cluster_name}">>./create_aws_instance_by_script.yml
	echo "vpc_id: ${v_create_aws_instance_vpc_id}">>./create_aws_instance_by_script.yml
	echo "image: ${v_create_aws_instance_image}">>./create_aws_instance_by_script.yml
	echo "zone: ${v_create_aws_instance_zone}">>./create_aws_instance_by_script.yml
	echo "vpc_subnet: ${v_create_aws_instance_vpc_subnet}">>./create_aws_instance_by_script.yml
	echo "aws_cluster_type: ${v_create_aws_instance_type}">>./create_aws_instance_by_script.yml
	echo "aws_cluster_count: ${v_create_aws_instance_count}">>./create_aws_instance_by_script.yml
	echo "aws_key_name: ${v_create_aws_instance_key_name}">>./create_aws_instance_by_script.yml
	echo "ansible_server_security_group: ansible_manager">>./create_aws_instance_by_script.yml
	echo "cluster_volumes:">>./create_aws_instance_by_script.yml
	echo "  - device_name: /dev/sda1">>./create_aws_instance_by_script.yml
	echo "    volume_type: gp2">>./create_aws_instance_by_script.yml
	echo "    volume_size: ${v_create_aws_instance_root_disk_size}">>./create_aws_instance_by_script.yml
	echo "    delete_on_termination: yes">>./create_aws_instance_by_script.yml

	for ((i=1; i<=${v_create_aws_instance_data_disk_count}; i++));
	do
	echo "  - device_name: /dev/sd${d_disk_info_mapping[$i]}">>./create_aws_instance_by_script.yml
	echo "    volume_type: gp2">>./create_aws_instance_by_script.yml
	echo "    volume_size: ${d_disk_size_mapping[$i]}">>./create_aws_instance_by_script.yml
	echo "    delete_on_termination: yes">>./create_aws_instance_by_script.yml
	echo "    encrypted: yes">>./create_aws_instance_by_script.yml
	done

	echo "cluster_device_path:">>./create_aws_instance_by_script.yml
	
	for ((i=1; i<=${v_create_aws_instance_data_disk_count}; i++));
	do
	echo " - { device_name: '/dev/xvd${d_disk_info_mapping[$i]}', target_path: '${d_disk_path_mapping[$i]}' }">>./create_aws_instance_by_script.yml
	done
	
	echo "">>./create_aws_instance_by_script.yml
	chmod 700 ./create_aws_instance_by_script.yml
	#########################################################################################
	read -p "Please input your choice:" debug_choice
	case $debug_choice in        
		[Rr]) return ;;
		[Xx]) exit 0 ;;
		   *) input_error_key;;
	esac

}

do_create_aws_instance_data_disk_info_sub_task() {

	clear
	echo -e "\nEntry the instance data disk info"
	echo -e "-------------------------------------------------------------------------------"
	echo -e "Please enter the size of your ${v_create_aws_instance_data_disk_count} disks in turn and the directory information you need to mount them."
	echo -e "e.g.  /data1 "
	echo -e ""
	echo -e " (r) Return"
	echo -e " (x) Exit"
	echo -e "-------------------------------------------------------------------------------"

	read -p "Please enter the size of your $1 disk in GB:" create_aws_instance_data_disk_info_choice
	case ${create_aws_instance_data_disk_info_choice} in        
	 [Rr]) return 2 ;;
	 [Xx]) exit 0 ;;
	    *) 
	    	if [[ "${create_aws_instance_data_disk_info_choice}"x == ""x ]]; then
	    		cannot_be_empty
	    		return 1
	    	fi	  
	    	 
	    	expr ${create_aws_instance_data_disk_info_choice} + 0 1>/dev/null 2>&1
			if [[ $? -ne 0 ]]; then
				not_a_valid_number
				return 1
			fi

			if [[ ! "${create_aws_instance_data_disk_info_choice}" -gt 0 ]]; then
				input_error_key
				return 1
			fi
			d_disk_size_mapping+=([$1]="${create_aws_instance_data_disk_info_choice}")
	    	;;
	esac
	
	read -p "Please enter the absolute path your $1 disk needs to be mounted:" create_aws_instance_data_disk_info_choice
	case $create_aws_instance_data_disk_info_choice in        
	 [Rr]) return 2 ;;
	 [Xx]) exit 0 ;;
	    *) 
	    	if [[ "${create_aws_instance_data_disk_info_choice}"x == ""x ]]; then
	    		cannot_be_empty
	    		return 1
	    	fi	
	    	    
	    	expr ${create_aws_instance_data_disk_info_choice} + 0 1>/dev/null 2>&1
			if [[ $? -eq 0 ]]; then
				input_error_key
				return 1
			fi

	    	if [[ "${create_aws_instance_data_disk_info_choice:0:1}"x != "/"x ]]; then
	    		input_error_key
	    		return 1
	    	fi

			d_disk_path_mapping+=([$1]="${create_aws_instance_data_disk_info_choice}")
	    	;;
	esac
}

do_create_aws_instance_data_disk_info() { 
	while true
	do
		d_disk_size_mapping=()
		d_disk_path_mapping=()
		rst=
		for ((i=1; i<=${v_create_aws_instance_data_disk_count}; i++));
		do
			do_create_aws_instance_data_disk_info_sub_task $i
			rst=$?
			while [[ $rst -eq 1 ]]
			do
				do_create_aws_instance_data_disk_info_sub_task $i
				rst=$?
			done

			if [[ $rst -eq 2 ]]; then
				return
			fi
		done
		debugging
	done
}

do_create_aws_instance_data_disk_count() {
	while true
	do
		clear
		echo -e "\nEntry the instance data disk count"
		echo -e "-------------------------------------------------------------------------------"
		echo -e "Please enter a number greater than 0 and less than or equal to 9."
		echo -e ""
		echo -e " (r) Return"
		echo -e " (x) Exit"
		echo -e "-------------------------------------------------------------------------------"
		read -p "Please input the instance data disk count:" create_aws_instance_data_disk_count_choice
		case $create_aws_instance_data_disk_count_choice in        
		 [Rr]) return ;;
		 [Xx]) exit 0 ;;
		    *) 
		    	if [[ "${create_aws_instance_data_disk_count_choice}"x == ""x ]]; then
		    		cannot_be_empty
		    		continue
		    	fi
		    	
		    	expr $create_aws_instance_data_disk_count_choice + 0 1>/dev/null 2>&1
				if [[ $? -ne 0 ]]; then
					not_a_valid_number
					continue
				fi

				if [[ ! "$create_aws_instance_data_disk_count_choice" -gt 0 ]]; then
					input_error_key
					continue
				fi
				
				if [[ "$create_aws_instance_data_disk_count_choice" -gt 9 ]]; then
					input_error_key
					continue
				fi
		    	v_create_aws_instance_data_disk_count=${create_aws_instance_data_disk_count_choice}
		    	do_create_aws_instance_data_disk_info
		    	;;
		esac
	done
}

do_create_aws_instance_root_disk_size() {
	while true
	do
		clear
		echo -e "\nEntry the instance root disk size(Unit GB)"
		echo -e "-------------------------------------------------------------------------------"
		echo -e "Please enter a number greater than zero"
		echo -e ""
		echo -e " (r) Return"
		echo -e " (x) Exit"
		echo -e "-------------------------------------------------------------------------------"
		read -p "Please input the instance root disk size:" create_aws_instance_root_disk_size_choice
		case $create_aws_instance_root_disk_size_choice in        
		 [Rr]) return ;;
		 [Xx]) exit 0 ;;
		    *) 
		    	if [[ "${create_aws_instance_root_disk_size_choice}"x == ""x ]]; then
		    		cannot_be_empty
		    		continue
		    	fi
		    	
		    	expr $create_aws_instance_root_disk_size_choice + 0 1>/dev/null 2>&1
				if [[ $? -ne 0 ]]; then
					not_a_valid_number
					continue
				fi

				if [[ ! "$create_aws_instance_root_disk_size_choice" -gt 0 ]]; then
					input_error_key
					continue
				fi
		    	v_create_aws_instance_root_disk_size=${create_aws_instance_root_disk_size_choice}
		    	do_create_aws_instance_data_disk_count
		    	;;
		esac
	done
}

do_create_aws_instance_key_name() {
	while true
	do
		clear
		echo -e "\nEntry the instance key pair name of the AWS"
		echo -e "-------------------------------------------------------------------------------"
		echo -e "Direct press Entry default selection: cdap_ha_cluster_key_1"
		echo -e ""
		echo -e "If you enter it manually, make sure that the key pair already exists in AWS"
		echo -e "otherwise you will get an error exit during the creation of the instance."
		echo -e ""
		echo -e " (r) Return"
		echo -e " (x) Exit"
		echo -e "-------------------------------------------------------------------------------"
		read -p "Please input the instance key pair name:" create_aws_instance_key_name_choice
		case $create_aws_instance_key_name_choice in        
		 [Rr]) return ;;
		 [Xx]) exit 0 ;;
		    *) 
		    	if [[ "${create_aws_instance_key_name_choice}"x == ""x ]]; then
		    		v_create_aws_instance_key_name="cdap_ha_cluster_key_1"
		    	else
		    		v_create_aws_instance_key_name=${create_aws_instance_key_name_choice}
		    	fi
		    	do_create_aws_instance_root_disk_size
		    	;;
		esac
	done
}

do_create_aws_instance_count() {
	while true
	do
		clear
		echo -e "\nEntry the instance count of the AWS"
		echo -e "-------------------------------------------------------------------------------" 
		echo -e "Please enter a number greater than zero"
		echo -e ""
		echo -e " (r) Return"
		echo -e " (x) Exit"
		echo -e "-------------------------------------------------------------------------------"
		read -p "Please input the instance count:" create_aws_instance_count_choice
		case $create_aws_instance_count_choice in        
		 [Rr]) return ;;
		 [Xx]) exit 0 ;;
		    *) 
		    	if [[ "${create_aws_instance_count_choice}"x == ""x ]]; then
		    		cannot_be_empty
		    		continue
		    	fi
		    	
		    	expr $create_aws_instance_count_choice + 0 1>/dev/null 2>&1
				if [[ $? -ne 0 ]]; then
					not_a_valid_number
					continue
				fi

				if [[ ! "$create_aws_instance_count_choice" -gt 0 ]]; then
					input_error_key
					continue
				fi
		    	v_create_aws_instance_count=${create_aws_instance_count_choice}
		    	do_create_aws_instance_key_name
		    	;;
		esac
	done
}

do_create_aws_instance_type_2() {
	while true
	do
		declare -A tmp_dict_type
		tmp_dict_type=()
		
		clear
		echo -e "\nSelect the instance type of the AWS"
		echo -e "-------------------------------------------------------------------------------" 
		
		if [[ "$1"x == "1"x ]]; then
			for i in "${!l_general_purpose[@]}"; do
				echo -e " ($i) ${l_general_purpose[$i]}"
				tmp_dict_type+=([$i]="${l_general_purpose[$i]}")
			done
		elif [[ "$1"x == "2"x ]]; then
			for i in "${!l_compute_optimized[@]}"; do
				echo -e " ($i) ${l_compute_optimized[$i]}"
				tmp_dict_type+=([$i]="${l_compute_optimized[$i]}")
			done
		elif [[ "$1"x == "3"x ]]; then
			for i in "${!l_memory_optimized[@]}"; do
				echo -e " ($i) ${l_memory_optimized[$i]}"
				tmp_dict_type+=([$i]="${l_memory_optimized[$i]}")
			done
		elif [[ "$1"x == "4"x ]]; then
			for i in "${!l_storage_optimized[@]}"; do
				echo -e " ($i) ${l_storage_optimized[$i]}"
				tmp_dict_type+=([$i]="${l_storage_optimized[$i]}")
			done
		elif [[ "$1"x == "5"x ]]; then
			for i in "${!l_accelerated_computing[@]}"; do
				echo -e " ($i) ${l_accelerated_computing[$i]}"
				tmp_dict_type+=([$i]="${l_accelerated_computing[$i]}")
			done
		elif [[ "$1"x == "6"x ]]; then
			for i in "${!l_bare_metal[@]}"; do
				echo -e " ($i) ${l_bare_metal[$i]}"
				tmp_dict_type+=([$i]="${l_bare_metal[$i]}")
			done
		fi
		
		echo -e ""
		echo -e " (r) Return"
		echo -e " (x) Exit"
		echo -e "-------------------------------------------------------------------------------"
		read -p "Please input your choice:" create_aws_instance_type_2_choice
		case $create_aws_instance_type_2_choice in        
		 [Rr]) return ;;
		 [Xx]) exit 0 ;;
		    *) 
		    	get_type=${tmp_dict_type[${create_aws_instance_type_2_choice}]}
		    	if [[ "${get_type}"x == ""x ]]; then
		    		input_error_key
		    		continue
		    	fi
		    	v_create_aws_instance_type=${tmp_dict_type[${create_aws_instance_type_2_choice}]}
		    	do_create_aws_instance_count
		    	;;
		esac
	done
}

do_create_aws_instance_type_1() {
	while true
	do
		clear
		echo -e "\nSelect the instance type of the AWS"
		echo -e "-------------------------------------------------------------------------------"
		echo -e " (1) General Purpose : "
		echo -e "     ${l_general_purpose[*]}\n"
		echo -e " (2) Compute Optimized : "
		echo -e "     ${l_compute_optimized[*]}\n"
		echo -e " (3) Memor Optimized : "
		echo -e "     ${l_memory_optimized[*]}\n"
		echo -e " (4) Storage Optimized : "
		echo -e "     ${l_storage_optimized[*]}\n"
		echo -e " (5) Accelerated Computing : "
		echo -e "     ${l_accelerated_computing[*]}\n"
		echo -e " (6) Bare Metal : "
		echo -e "     ${l_bare_metal[*]}"
		echo -e ""
		echo -e " (r) Return"
		echo -e " (x) Exit"
		echo -e "-------------------------------------------------------------------------------"
		read -p "Please input your choice:" create_aws_instance_type_1_choice
		case $create_aws_instance_type_1_choice in        
		 [Rr]) return ;;
		 [Xx]) exit 0 ;;
		    1) do_create_aws_instance_type_2 1 ;;
		    2) do_create_aws_instance_type_2 2 ;;
		    3) do_create_aws_instance_type_2 3 ;;
		    4) do_create_aws_instance_type_2 4 ;;
		    5) do_create_aws_instance_type_2 5 ;;
		    6) do_create_aws_instance_type_2 6 ;;
		    *) input_error_key;;
		esac
	done
}

do_create_aws_instance_zone() {
	while true
	do
		declare -A tmp_dict_zone
		tmp_dict_zone=()
		
		clear
		echo -e "\nSelect the Zone of the AWS"
		echo -e "-------------------------------------------------------------------------------" 
		
		if [[ "${v_create_aws_instance_region}"x == "us-west-2"x ]]; then
			i=1
			for key in $(echo ${!d_zone_vpc_subnet_oregon[*]})
			do
    			echo -e " ($i) ${key}"
    			tmp_dict_zone+=([$i]="${key}")
    			((i++))
			done
		elif [[ "${v_create_aws_instance_region}"x == "ap-southeast-1"x ]]; then
			i=1
			for key in $(echo ${!d_zone_vpc_subnet_singapore[*]})
			do
    			echo -e " ($i) ${key}"
    			tmp_dict_zone+=([$i]="${key}")
    			((i++))
			done
		else
			echo -e "There is no active zone in this Region, Please return. "
		fi
		
		echo -e ""
		echo -e " (r) Return"
		echo -e " (x) Exit"
		echo -e "-------------------------------------------------------------------------------" 
		read -p "Please input your choice:" create_aws_instance_zone_choice
		case $create_aws_instance_zone_choice in        
		 [Rr]) return ;;
		 [Xx]) exit 0 ;;
		    1) 
				if [[ "${v_create_aws_instance_region}"x == "us-west-2"x ]]; then
		    		v_create_aws_instance_zone=${tmp_dict_zone["1"]}
		    		v_create_aws_instance_vpc_subnet=${d_zone_vpc_subnet_oregon[${tmp_dict_zone["1"]}]}
		    		do_create_aws_instance_type_1
				elif [[ "${v_create_aws_instance_region}"x == "ap-southeast-1"x ]]; then
		    		v_create_aws_instance_zone=${tmp_dict_zone["1"]}
		    		v_create_aws_instance_vpc_subnet=${d_zone_vpc_subnet_singapore[${tmp_dict_zone["1"]}]}
		    		do_create_aws_instance_type_1
				fi
		    	;;
		    2)
				if [[ "${v_create_aws_instance_region}"x == "us-west-2"x ]]; then
		    		v_create_aws_instance_zone=${tmp_dict_zone["2"]}
		    		v_create_aws_instance_vpc_subnet=${d_zone_vpc_subnet_oregon[${tmp_dict_zone["2"]}]}
		    		do_create_aws_instance_type_1
				elif [[ "${v_create_aws_instance_region}"x == "ap-southeast-1"x ]]; then
		    		v_create_aws_instance_zone=${tmp_dict_zone["2"]}
		    		v_create_aws_instance_vpc_subnet=${d_zone_vpc_subnet_singapore[${tmp_dict_zone["2"]}]}
		    		do_create_aws_instance_type_1
				fi
		    	;;
		    *) input_error_key;;
		esac
	done
}

do_create_aws_instance_region() {
	while true
	do
		clear
		echo -e "\nSelect the Region of the AWS"
		echo -e "-------------------------------------------------------------------------------"
		echo -e " (1) Oregon"
		echo -e " (2) Singapore" 
		echo -e ""
		echo -e " (r) Return"
		echo -e " (x) Exit"
		echo -e "-------------------------------------------------------------------------------" 
		read -p "Please input your choice:" create_aws_instance_region_choice
		case $create_aws_instance_region_choice in        
		 [Rr]) return ;;
		 [Xx]) exit 0 ;;
		    1) 
		    	v_create_aws_instance_region=${d_region_oregon["region"]}
				v_create_aws_instance_vpc_id=${d_region_oregon["vpc_id"]}
				v_create_aws_instance_image=${d_region_oregon["image"]}
				do_create_aws_instance_zone
				;;
		    2) 
		    	v_create_aws_instance_region=${d_region_singapore["region"]}
				v_create_aws_instance_vpc_id=${d_region_singapore["vpc_id"]}
				v_create_aws_instance_image=${d_region_singapore["image"]}
				do_create_aws_instance_zone
				;;
		    *) input_error_key;;
		esac
	done
}

do_create_aws_instance_cluster_name() {
	while true
	do
		clear
		echo -e "\nEnter the cluster name"
		echo -e "-------------------------------------------------------------------------------"
		echo -e ""
		echo -e " (r) Return"
		echo -e " (x) Exit"
		echo -e "-------------------------------------------------------------------------------" 
		read -p "Please input your cluster name:" create_aws_instance_cluster_name_choice
		case $create_aws_instance_cluster_name_choice in        
		 [Rr]) return ;;
		 [Xx]) exit 0 ;;          
		    *) 
		    	if [[ "${create_aws_instance_cluster_name_choice}"x == ""x ]]; then
		    		cannot_be_empty
		    		continue
		    	fi
		    		
		    	v_create_aws_instance_cluster_name=$create_aws_instance_cluster_name_choice
		    	v_create_aws_instance_cluster_security_group_name=${v_create_aws_instance_cluster_name}_group
		    	do_create_aws_instance_region
		    	;;
		esac
	done
}

# To startup
while true
do
	clear
	echo -e "\nAutomate operations scripts"
	echo -e "-------------------------------------------------------------------------------"
	echo -e " (1) Create the new AWS instances"
	echo -e ""
	echo -e " (x) Exit"
	echo -e "-------------------------------------------------------------------------------"  
	read -p "Please input your choice:" startup_choice
	case $startup_choice in
	    1) do_create_aws_instance_cluster_name ;; 
	 [Xx]) exit 0 ;;
	    *) input_error_key ;;
	esac
done

