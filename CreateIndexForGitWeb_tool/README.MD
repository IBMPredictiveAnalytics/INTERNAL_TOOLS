	Tool Name:	CreateIndexForDownloadExtension
	
	Platform： Windows
	
	Description:	This tool is automatically used to create index.json for download extension. The python version is 3.4.3
	
	Usage: 		CreateIndexForDownloadExtension [options] arg1 arg2 arg3

				Options:

					-h, --help          show help message and exit  

					-s, --spedir        Directory to save spe.

					-o, --output        Choose a dir to save index file.

					-p, --product       Choose index for which product: 1. modeler 2. stats. //Currently there are only two products name here.
                   
    How to run:	
    
          1. Open cmd dialog

	  2. Input following command. Replace your own directories to save .spe file and index file
	          
                python CreateIndexForDownloadExtension.py -s "C:\spe" -o "C:\index" -p stats            
