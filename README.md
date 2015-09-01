# INTERNAL_TOOLS
Hold internal tools for repository maintaining and index for website and products

Tools Index:

1. 	Tool Name:	CreateIndexForGithubWeb

	Description:	This tool is automatically used to create index_for_web.json for github website. The python version is 3.4.3
   
	How to run:	1)  Before running the script, please set your local path for variable "index_for_web_path" 
                     in the script. 
                   
                2)  Then, put 'index_for_web.json' to .io repository.
				 

2. 	Tool Name:	CreateIndexForDownloadExtension
	
	Description:	This tool is automatically used to create index.json for download extension. The python version is 3.4.3
	
	Usage: 		CreateIndexForDownloadExtension [options] arg1 arg2 arg3

				Options:

					-h, --help          show help message and exit  

					-s, --spedir        Directory to save spe.

					-o, --output        Choose a dir to save index file.

					-p, --product       Choose index for which product: 1. modeler 2. stats. //Currently there are only two products name here.
                   
    How to run:	input command in Windows cmd,

					python CreateIndexForDownloadExtension.py -s "C:\spe" -o "C:\index" -p stats            
