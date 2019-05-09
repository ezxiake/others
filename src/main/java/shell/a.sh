<<<<<<< HEAD
#!/bin/bash
#--------------------------------------------------------------------
# Fuction£º³ÌÐòÆôÍ£½Å±¾
# Version: 1.0
# Created: ****
# Created date:2017/11/14
# Modify history:
#--------------------------------------------------------------------

trap '' 2 3 15 20
 
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
		    y) return 0 ;;
		    n) return 1 ;;
		    *) input_error_key ;;
		esac
	done
}
 
 

create_aws_instance_menu() {
	v_create_aws_instance_cluster_name=
	v_create_aws_instance_cluster_security_group_name=
	v_create_aws_instance_region=
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
		    r) return ;;             
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

	while true
	do
		clear
		echo -e "\n-----------------Create the new AWS instance or instances-----------------"  
		echo -e " cluster name : ${v_create_aws_instance_cluster_name}"
		echo -e " cluster security group name : ${v_create_aws_instance_cluster_security_group_name}"
		echo -e " region : "
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
		read -p "Please input your region:" choice
		case $choice in        
		    r) return ;;             
		    *) continue ;;
		esac
	done
}

# To startup
while true
do
	clear
	echo -e "\n-----------------Automate operations scripts-----------------"  
	echo -e " (0) Create the new AWS instance or instances" 
	echo -e " (x) Exit"
	echo -e " ----------------------------------"  
	read -p "Please input your choice:" choice
	case $choice in
	    0) create_aws_instance_menu ;; 
	    x) exit 0 ;;             
	    *) input_error_key ;;
	esac
done
=======
#!/bin/bash
#--------------------------------------------------------------------
# Fuction
# Version: 1.0
# Created: ****
# Created date:2017/11/14
# Modify history:
#--------------------------------------------------------------------

trap '' 2 3 15 20
 
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
		    y) return 0 ;;             
		    n) return 1 ;;
		    *) input_error_key ;;
		esac
	done
}
 

create_aws_instance_menu() {
	v_create_aws_instance_cluster_name=
	v_create_aws_instance_cluster_security_group_name=
	v_create_aws_instance_region=
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
		    r) return ;;             
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

	while true
	do
		clear
		echo -e "\n-----------------Create the new AWS instance or instances-----------------"  
		echo -e " cluster name : ${v_create_aws_instance_cluster_name}"
		echo -e " cluster security group name : ${v_create_aws_instance_cluster_security_group_name}"
		echo -e " region : "
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
		read -p "Please input your region:" choice
		case $choice in        
		    r) return ;;             
		    *) continue ;;
		esac
	done
}

# To startup
while true
do
	clear
	echo -e "\n-----------------Automate operations scripts-----------------"  
	echo -e " (0) Create the new AWS instance or instances" 
	echo -e " (x) Exit"
	echo -e " ----------------------------------"  
	read -p "Please input your choice:" choice
	case $choice in
	    0) create_aws_instance_menu ;; 
	    x) exit 0 ;;             
	    *) input_error_key ;;
	esac
done
>>>>>>> branch 'master' of https://github.com/ezxiaoke/shell.git
