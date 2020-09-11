# This is the set of python3 scripts used to perform some checks GCP Project Resources to improve security
-------------

This script is worked for individual GCP project not on organization or folder level

package installation
    
    install package using 
    pip3 install gcpsecurity

How to use ??

    step 1: Import classes to perform checks
        
        from gcpsecurity.gcp_vm import ExecuteCheckVm
        from gcpsecurity.gcp_iam import ExecuteCheckIam
        from gcpsecurity.gcp_vpc import ExecuteCheckVpc
        from gcpsecurity.gcp_gcs import ExecuteCheckGcs
        from gcpsecurity.gcp_cloud_sql import ExecuteCheckSql
            
    step 2: Create GCP service account with project viewer permission
    step 3: Initlize ExecuteCheck class with service account file path and project id
            
            vm = ExecuteCheckVm(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            vpc = ExecuteCheckVpc(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            iam = ExecuteCheckIam(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            gcs = ExecuteCheckGcs(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
            sql = ExecuteCheckSql(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
    
    step 4: Call perform_check() method of ExecuteCheck classes object
    
            vm_result = vm.perform_check()
            vpc_result = vpc.perform_check()
            iam_result = iam.perform_check()
            gcs_result = gcs.perform_check()
            sql_result = sql.perform_check()
    
    step 5: Print results
            
            print(vm_result)
            print(vpc_result)
            print(iam_result)
            print(gcs_result)
            print(sql_result)
              
    
 
**note:- service account file should have appropriate permissions to perform checks 
That is Project Viewer (You can set permissions as per service also)

    