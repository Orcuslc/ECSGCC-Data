<head>
<style type="text/css">
body {font-family: Consolas;}
</style>
</head>
# <font color=#0099ff size = 20 face="Consolas"> Read Me :+1:</font>

<font color=#0099ff size=6 face="Consolas"> About The Module</font>

<font face = "Consolas">In this module, we use SVR model to perform max daily load prediction. 
The module consists of three sub-folders: 
`/src`: Source codes:
&emsp;&emsp; `/conf.py`: configuration file
&emsp;&emsp; `/prep_attr.py`: functions for preparing attributes for prediction
&emsp;&emsp; `/predict.py`: containing a class of Predictor
`/util`: Utilities:
&emsp;&emsp; `/one_step_predict.py`: functions for /one-step prediction
&emsp;&emsp; `/multi_step_prediction.py`: functions for multi-step prediction
`/data`: Data for prediction
</font>
---

<font color=#0099ff size=6 face="Consolas"> Dependency</font>
<font face="Consolas">
&emsp;&emsp; Python 3.0+
&emsp;&emsp; scikit-learn
&emsp;&emsp; numpy
&emsp;&emsp; matplotlib
&emsp;&emsp; pandas
</font>

---
<font color=#0099ff size=6 face="Consolas"> Usage</font>
<font face="Consolas">
1. Go to `/src/conf.py` and change the configuration info there. Notice: The configuration for `predict.py` should not be changed.
2. Write information in `/data/simp_daily_data.csv` or the path you write in (1). The data structure should be as follows:
`date(2016/01/01), yesterday's max load(26000), today's average temperature(29.0), weekday(1~7), holiday(1 for weekends, 0 for non-holidays, -1 for long holidays)`
Notice: Always keep an empty line at the end of the file.		
3. Go to `/util`, open the console and 
&emsp;&emsp; `python3 one_step_predict.py ATTR_PATH`.
If attr is wrote in `ATTR_PATH` in (1), then `ATTR_PATH` is not necessary.
</font>
---

<font color=#0099ff size=6 face="Consolas"> Contributor</font>
<font face="Consolas">
Chuan Lu
Homepage: http://chuanlu.xyz
GitHub: https://github.com/orcuslc
Email: chuanlu13@fudan.edu.cn