Tool Name:      CreatePackage

Platform:       Windows

Requirement:    Python3.4.3

Description:    This tool is automatically used to create zip package for stats extensions.

Usage:          python main.py [options] arg1 arg2

Options:

    -o, --output        Choose a dir to save index_for_web.json file.
    
    -p, --product       Choose the which product: 1. stats 2. modeler. Any other string can lead to an error.  

How to run: 

    1. Download CreatePackage project to local machine
    
    2. Generate your own token for get release information. How to generate the token?
    
    https://help.github.com/articles/creating-an-access-token-for-command-line-use/
    
    3. In line 8th of CreatePackage/CreateExtensionIndex/GetLatestTag.py where "TOKEN = ''", write the token got in step 2. 

    4. Open cmd dialog.

    5. Input following command in the dialog. Set your own directory to save index_for_web json.

        python C:\CreatePackage\main.py -o "C:\Users\your_directory" -p stats       
