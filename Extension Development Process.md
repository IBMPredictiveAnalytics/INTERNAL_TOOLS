# IBM Predictive Analytics Extension Development
---
This guide help IBM SPSS Modeler/Statistics user contribute the extension they developed. Then public to [IBM Predictive Analytics](http://ibmpredictiveanalytics.github.io/) hub site. And also public to Modeler/Statistics extension hub.

## Install IBM SPSS Modeler/Statistics
---
Install IBM SPSS Modeler/Statistics  
[IBM SPSS Modeler](https://www.ibm.com/marketplace/cloud/spss-modeler/us/en-us?S_TACT=M161007W)  
[IBM SPSS Statistics](https://www.ibm.com/marketplace/cloud/statistical-analysis-and-reporting/us/en-us?S_TACT=M161007W)

## Install IBM SPSS Modeler/Statistics Extension
---
Install IBM SPSS Modeler/Statistics Extension  
[Download Extension](https://developer.ibm.com/predictiveanalytics/downloads/)

## Develop extension
---
This part focus on extension development. For detail about extension develop, please read Modeler/Statistics `Help` document.

### Custom dialog builder
Open `Custom Dialog Builder` through `Extensions -> Custom Node Dialog Builder` (Modeler) or `Extensions -> Custom Dialog Builder for Extension` (Statistics).  
Then start build self-defined dialog.

### R/Python script
IBM SPSS Modeler/Statistics support R/Python as program language. Please make sure IBM SPSS Modeler/Statistics R/Python extension installed. Then follow below step:   
- Develop script out of `Custom Dialog Builder`.  
- Add data/output handle part to final script.
- Paste developed script to `Custom Dialog Builder` 's `Script` part.
- Paste score script to `Score Script` part if necessary.

### Handle dialog input
In `Custom Dialog Builder`, when select UI element, `Property` part show under the dialog. The config 
1. `Identifier` cell to define a identifier name.
2. `Script` cell to define how to use input value. 
 - For "Field Chooser" or "Text Control", use `%%ThisValue%%` to represent user input value. 
 - For "Check Box", use `"value"` means to represent constant value. 
3. In script, use `%%identifier_name%%` to pass those UI element input to R/Python script.

### Handle data
Extension can use pre-defined dataset from Modeler/Statistics like `ModelerData`, `StatisticsData`. More detail please refer to help document.

### Handle output(statistical chart)
Please refer to help document.

### Dialouge properity
In `Custom Dialog Builder`, open `Extension -> Properties` to open `Extension Properties` dialog. Fill all required part, which include
- Name
- Summary
- Version
- Mininum Version
- Files

### Install and test extension
to do

## Put extension to github
Currently, all extension are hosted in [git](hubhttps://github.com/IBMPredictiveAnalytics) now. 

### Rule of repo name
No space, use "_" to between two words.

If want contribute extension, please follow below step
1. Create self repo in github 
2. Ask admin of IBMPredictiveAnalytics to fork your repo to IBMPredictiveAnalytics.

## Public extension

Please fork [IBMPredictiveAnalytics.github.io](https://github.com/IBMPredictiveAnalytics/IBMPredictiveAnalytics.github.io) when want public extension.

### Public extension to Gallery
2. Clone IBMPredictiveAnalytics.github.io to local.
3. Change `resbundles\index_for_web.json`, add below value to this json file.
 - repository:
 - description:
 - pushed_at:
 - provider:
 - software:
 - language:
 - category:
 - promotion:
```xml
    {
		"repository":"Alchemy_Text_Sentiment",
		"description":"This extension use Alchemy Text Sentiment API for computing document-level sentiment",
		"pushed_at":"2016-06-29T13:11:13Z",
		"type":"Extension",
		"provider":"IBM",
		"software":"SPSS Modeler",
		"language":" R",
		"category":"Utility",
		"promotion":"No"
    }
```
4. Push to github and submit a pull request to 

### Public extension to Extension hub
to do

## IBMPredictiveAnalytics commiter
Greg Filla [(mail to)](mailto:)  
Yu Wenpei [(mail to)](mailto:yuwenp@cn.ibm.com)