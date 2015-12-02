'''
Created on Oct 27, 2015

@author: wujz
'''
from CreateExtensionIndex.createExtensionIndex import createExtensionIndex

if __name__ == '__main__':            
    # Currently this script is only used for stats
    # if options.productName.lower() != "modeler" and options.productName.lower() != "stats":  
    #     parser.error("Please input valid product name modeler or stats (casesensitive) for your index file")
    
    try:
        createExtensionIndex('C:\\Users\\wujz\\Desktop\\modelertest', 'modeler')
    except IOError as e:
        print(str(e))
    except Exception as e:
        print(str(e)) 