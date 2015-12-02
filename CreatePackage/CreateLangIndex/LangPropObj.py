'''
Created on Oct 27, 2015

@author: wujz
'''
from common.JSONObj import JSONObj
from configparser import ConfigParser
INDENT = '\t'
LANG_JSON_KET = ['Name', 'Summary', 'Description']

class LangPropObj:
    @staticmethod
    def convertToJSONStr(repo_name, propStr, lang_item):
        config = ConfigParser()
        con = '[tag]\n'+propStr
        config.read_string(con)
        
        for item in config.sections():
            jsonStr = INDENT*2+'{\n'+INDENT*3+JSONObj.createJSONStr(LANG_JSON_KET[0],repo_name)
            
            for key in LANG_JSON_KET[1:]:
                if key.lower() in config.options(item):
                    jsonStr += INDENT*3+JSONObj.createJSONStr(key, config.get(item, key))
                else:
                    raise Exception("FormatError: "+key+" is not a legal key in lang properties file of "+repo_name+"-"+lang_item+". Please check!")
        
        return jsonStr[0:-2]+'\n'+INDENT*2+'},\n'
    
    @staticmethod
    def generateJSONStr(name, summary, descr):
        json_str = INDENT*2+'{\n'
        json_str += INDENT*3 + JSONObj.createJSONStr(LANG_JSON_KET[0], name)
        json_str += INDENT*3 + JSONObj.createJSONStr(LANG_JSON_KET[1], summary)
        json_str += INDENT*3 + JSONObj.createJSONStr(LANG_JSON_KET[2], descr)
        return json_str[0:-2]+'\n'+INDENT*2+'},\n'
        