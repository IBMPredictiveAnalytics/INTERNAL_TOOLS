# Public Extension to Extension Hub

IBM SPSS Modeler/Statistics Extension allow user to public they own extension to Extension Hub base on Apache 2.0 License. This instruction help extension developer prepare they extension for publication.  
Extension developer should ensure below requirement, then ask IBM Predictive Analytics administrator FORK your repository to  IBMPredictiveAnalytics organization.

Currently, publication means show extension in below:
- IBM Predictive Analytics [Gallery ](http://ibmpredictiveanalytics.github.io/)
- IBM SPSS Modeler/Statistics Extension Hub. Provider auto installation framework for GitHub hosted extension.

---
## Requirement

### Logo
[Extension Gallery](http://ibmpredictiveanalytics.github.io/) need a logo for extension exhibition.   
- Size: 320px * 180px
- Background: Transparent or White
- Example: [1](https://raw.githubusercontent.com/IBMPredictiveAnalytics/Concept_Cloud_Visualization/master/default.png)

### Name
Extension Hub need extension has consistent name in below three part. Assume extension name is "YourExtensionName"
- Repository name. GitHub repository like https://github.com/yourname/YourExtensionName
- Extension file name. And extension file is YourExtensionName.mpe
- Extension name. Set extension name in extension properties.

### Info
Add info.json file to root of your repository with below information:
```xml
{
 "type": [ "Extension" ],
 "provider": [ "IBM" ],
 "software": [ "SPSS Modeler" ],
 "language": [ "R" ],
 "category": [ "Utility" ],
 "promotion": [ "No" ]
}
```
Please let administrator to review this to fit in correct value.

---
## Fork repository to IBMPredictiveAnalytics organization

Ask IBMPredictiveAnalytics organization administrator to fork you repository to that organization.

Administrator currently:
- Modeler:
Yu Wenpei [(mail to)](mailto:yuwenp@cn.ibm.com)
- Statistics:
Wu Jiazhong [(mail to)](mailto:wujz@cn.ibm.com)

---
## Release your extension
After fork, administrator can add you as Collaborators to IBMPredictiveAnalytics's repository. If you want public your extension to Extension Hub, it's necessary step.
In IBMPredictiveAnalytics's repository, click "release" button to entry release page. Except version number, title, describle, please add extension file (*.mpe) to release package.
Final release shoulb look like [this](https://github.com/IBMPredictiveAnalytics/SPSS_Moving_Average/releases)

### Version rule
{Major release}.{Fix pack release}.{Defect fix release}

---
## Fix defect
Since your are collaborators for both your repository and IBMPredictiveAnalytics's repository, it up to you to maintain IBMPredictiveAnalytics's repository only, or both.

### Maintain IBMPredictiveAnalytics's repository only
Commit your fix to IBMPredictiveAnalytics's repository directly

### Maintain both
 - Commit your fix to your repository,  
 - Send pull requrest to IBMPredictiveAnalytics, which base on IBMPredictiveAnalytics and head is yours,
 - Merge pull requrest

### Release new version 
After defect fix, please release new version to your extension.

---
### Public extension to Gallery and Extension Hub
Ask IBMPredictiveAnalytics organization administrator to public your extension.

Administrator currently:
- Modeler:
Yu Wenpei [(mail to)](mailto:yuwenp@cn.ibm.com)
- Statistics:
Wu Jiazhong [(mail to)](mailto:wujz@cn.ibm.com)