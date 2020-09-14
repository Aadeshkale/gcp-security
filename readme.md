# This Package helps to improve GCP project security and reduce billing from unused resources by performing some checks 

This script is worked for individual GCP project not on organization or folder level
__________


package installation
    
    pip3 install gcpsecurity

Ensure google cloud platform API is enable for particular service on which you want to perform check
   
    example,
    
    Enable api for data proc
    Enable api for app engine ...etc
    

How to use ??

    step 1: Import classes to perform checks
        
        from gcpsecurity.gcp_vm import ExecuteCheckVm
        from gcpsecurity.gcp_iam import ExecuteCheckIam
        from gcpsecurity.gcp_vpc import ExecuteCheckVpc
        from gcpsecurity.gcp_gcs import ExecuteCheckGcs
        from gcpsecurity.gcp_cloud_sql import ExecuteCheckSql
        from gcpsecurity.gcp_app_engine import ExecuteCheckGae
        from gcpsecurity.gcp_data_proc import ExecuteCheckDp
                 
    step 2: Create GCP service account with project viewer permission
    step 3: Initlize ExecuteCheck class with service account file path and project id
            
            vm = ExecuteCheckVm(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            vpc = ExecuteCheckVpc(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            iam = ExecuteCheckIam(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            gcs = ExecuteCheckGcs(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            sql = ExecuteCheckSql(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            gae = ExecuteCheckGae(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            dp = ExecuteCheckDp(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)

    
    step 4: Call perform_check() method of ExecuteCheck classes object
    
            vm_result = vm.perform_check()
            vpc_result = vpc.perform_check()
            iam_result = iam.perform_check()
            gcs_result = gcs.perform_check()
            sql_result = sql.perform_check()
            gae_result = gae.perform_check()
            dp_result = dp.perform_check()
    
    step 5: Print results
            
            print(vm_result)
            print(vpc_result)
            print(iam_result)
            print(gcs_result)
            print(sql_result)
 
              
Example script - https://github.com/Aadeshkale/gcp-security/blob/master/main.py 
 
 
** Note:- service account file should have appropriate permissions to perform checks 
That is Project Viewer (You can set permissions as per service also)


** Note :-Script might take time to execute because it is make googleapis calls


** To add other checks as per your use got to package gcpsecurity add checks in existing services scripts or add new scripts for new services

reference :- https://github.com/Aadeshkale/gcp-security/tree/master/gcpsecurity 