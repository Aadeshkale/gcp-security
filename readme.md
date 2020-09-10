# This is the set of python3 scripts perform some security check on your GCP Resources

You need to pass GCP Service account file,Project id wth appropriate permissions to script and it will generate csv report for you


Example,
    You want perform checks on GCP compute engine instances
    
    
    Then install required packages using 
    pip3 install -r requirements.txt
    
    Then use gcp_vm.py and set following variabls with appropriate values and permissions 
    
    PROJECT_ID = "example-284008"
    SERVICE_ACCOUNT_FILE_PATH = "my_credentials.json"

    Then run python3 gcp_vm.py,
     
    it will generate gcp_vm.csv file you can analize or you can use it in your project
    
    **note:- service account file should have appropriate permissions to perform checks 
    That is Project Viewer (You can set permissions as per service also)
