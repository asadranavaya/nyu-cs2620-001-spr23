# nyu-cs2620-001-spr23
 Collection of scripts to run for NMS capstone project
 
 VM's were run in the following cloud providers in the following regions:
 1. AWS
 
	1.a. Oregon
	
	1.b. Ohio
	
	1.c. Northen California
	
	1.d. Frankfurt, Germany
	
	1.e. Sao Paulo, Brazil
	
	1.f. Stockholm, Europe
	
2. GCP

	2.a. Asia-East-1-a
	
	2.b. Australia-southeast1-a 
	
	2.c. Europe-north1-b 
	
	2.d. Us-central1-f 
	
	2.e. US-south1-b 
	
3. AZURE

	3.a. Brazil South
	
	3.b. France Central
	
	3.c. Qatar Central
	
	3.d. South Africa North 
	
	3.e. Japan East 

Procedure:

	Setup:
	
		On each VM ensure that network security protocols allow for ICMP anywhere, ALL TCP, and ALL UDP. The server cannot send node location files if TCP anywhere is not set up.
		
		1. On each AWS vm running Amazon Linux, install pip for python package management.
		
			1.a Use: curl -O https://bootstrap.pypa.io/get-pip.py
			
			1.b Then use: python3 get-pip.py --user
			
			1.c Then use: sudo pip3 install requests
			
			1.d Then use: sudo pip3 install pythonping
			
		2. Then transfer python scripts to VM user folder, ensure the root folder has 777 privelages
		
		3. Run SERVER node first! Client nodes will look for server connection. Server node also dictates how many nodes will be in the experiment.
		
		4. Start each client node with elevated privelages (pythonping package requires root access)
		
			4.a. sudo python3 setup_node.py
			
