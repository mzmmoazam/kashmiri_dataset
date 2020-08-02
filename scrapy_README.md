# This tool is built using scrapy

## To list all spiders

`scrapy list`

```
gag_dict_spyder
kashmir_language_spyder
kashmiri_zabaan_spyder
sh_dict_spyder
```

### Note: There are different ways to run a spider to get data in different formats, check scrapy docs for more info

### Check the doc strings to see how to run spider

### Example

  To run `gag_dict_spyder` got to `kashmiri_dataset\spiders\ddsa_GAG_spyder.py` and there you would find
```
'''
    George A. Grierson
    Digital Dictionaries of South Asia
    
    usage :
        scrapy crawl gag_dict_spyder -o csv_files/file_name.csv
        
'''
```

---
