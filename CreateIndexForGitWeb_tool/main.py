# -*- coding: utf-8 -*-  
import os
import sys
import CreateIndexForGithubWeb
from optparse import OptionParser 

if __name__ == '__main__':
    usage = "usage: %prog [options] arg1 arg2"  
    parser = OptionParser(usage)  
    parser.add_option("-o", "--output", dest="outdir", action='store', help="Choose a dir to save index_for_web file.")
    parser.add_option("-g", "--gitbash", dest="gitbash", action='store', help="Git Bash")
    (options, args) = parser.parse_args() 
    
    if getattr(options, 'outdir') == None or not os.path.isdir(options.outdir):
        parser.error("Please input a valid directory to save index_for_web.json file\n\n")  
    else:
        index_for_web_path = os.path.join(options.outdir,CreateIndexForGithubWeb.INDEX_NAME)
           
    if getattr(options, 'gitbash') == None or not os.path.exists(options.gitbash):
        parser.error("Please input shell client path.\n")
        exit(1)
    git_bash = options.gitbash
    
    print("The index_for_web.json is saved in:"+index_for_web_path)
    try:
        CreateIndexForGithubWeb.createIndexForWeb(index_for_web_path)
    except Exception as e:
        print(str(e))
        sys.exit(-1)
    print("Cannot get below repositories information. Please check!")
    CreateIndexForGithubWeb.printError(CreateIndexForGithubWeb.UNICODE_ERROR_LIST, "UnicodeDecodeError")
    CreateIndexForGithubWeb.printError(CreateIndexForGithubWeb.HTTP_ERROR_LIST, "HTTPError")
    CreateIndexForGithubWeb.printError(CreateIndexForGithubWeb.VALUE_ERROR_LIST, "ValueError")
    CreateIndexForGithubWeb.printError(CreateIndexForGithubWeb.OTHER_ERROR_LIST, "Other exception")
    
    os.system(git_bash+" --login -i ./upload_web_index.sh "+index_for_web_path+" 'test upload script.' "+options.outdir)