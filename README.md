#Ethnicity of Group
Brendan J. Herger
hergertarian.com
13herger@gmail.com

##Usage
###Command line
The script is pretty straight forward. To use it on command line, use a 
command like:

```
python names_to_ethnicities.py --data_path test_data/test_names.txt
```

or change ```test_data/test_names.txt``` to ```any/path/youd/like```

This will output the results, in a form like: 

|white|45.782
|black|7.716
|asian_pac_islander|38.510
|american indian|0.212
|two+|1.866
|hispanic|5.728
dtype: float64




###File / Pandas DataFrame
Pretty straight forward. Use the sum_ethnicity_from_file() and
sum_ethnicity_from_df() methods.