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
        
        from gcpsecurity.gcp_data_proc import ExecuteCheckDp
        from gcpsecurity.gcp_gke import ExecuteCheckGke
                 
    step 2: Create GCP service account with project viewer permission
    step 3: Initlize ExecuteCheck class with service account file path and project id
            
        dp = ExecuteCheckDp(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
        gke = ExecuteCheckGke(servive_account_file_path=SERVICE_ACCOUNT_FILE_PATH, project_id=PROJECT_ID)
             
    
    step 4: Call perform_check() method of ExecuteCheck classes object
    
            dp_result = dp.perform_check()
            gke_result = gke.perform_check()
    
    step 5: Print results
            
            print(dp_result)
            print(gke_result)

Available services checks classes:
        
        compute engine checks ==> from gcpsecurity.gcp_vm import ExecuteCheckVm
        IAM checks            ==> from gcpsecurity.gcp_iam import ExecuteCheckIam
        VPC checks            ==> from gcpsecurity.gcp_vpc import ExecuteCheckVpc
        cloud storage         ==> from gcpsecurity.gcp_gcs import ExecuteCheckGcs
        cloud sql             ==> from gcpsecurity.gcp_cloud_sql import ExecuteCheckSql
        app engine            ==> from gcpsecurity.gcp_app_engine import ExecuteCheckGae
        data proc             ==> from gcpsecurity.gcp_data_proc import ExecuteCheckDp
        kubernetes engine     ==> gcpsecurity.gcp_gke import ExecuteCheckGke
 
              
Example script

        https://github.com/Aadeshkale/gcp-security/blob/master/main.py 
 
 
** Notes :-

1) Script might take time to execute because it is make googleapis calls.


2) Service account file should have appropriate permissions to perform checks That is Project Viewer (You can set permissions as per service also)


3) To add other checks as per your use go to package gcpsecurity add checks in existing services scripts or add new scripts for new services
reference :- https://github.com/Aadeshkale/gcp-security/tree/master/gcpsecurity 