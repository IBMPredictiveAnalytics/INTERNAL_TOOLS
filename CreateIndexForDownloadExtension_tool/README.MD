  Tool Name:	CreateIndexForDownloadExtension
  
  Platform:   Windows
  
  Requirement: Python3.4.3
	
  Description:	This tool is automatically used to create index.json for download extension. The python version is 3.4.3
	
  Usage: 		  CreateIndexForDownloadExtension [options] arg1 arg2 arg3

  Options:

	-h, --help          show help message and exit  

	-s, --spedir        Directory to save spe.

	-o, --output        Choose a dir to save index file.

	-p, --product       Choose index for which product: 1. modeler 2. stats. 
                   
  How to run:	
  
	1. Download CreateIndexForDownloadExtension.py.
      
	2. Open cmd dialog.
      
	3. Input below command. Set your own directory ro save .spe, index file, and product name.

	       python CreateIndexForDownloadExtension.py -s "C:\spe" -o "C:\index" -p stats   
