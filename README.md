# Group Project MSBD 5003
## Introduction

Dataset [Trending YouTube Video Statistics](https://www.kaggle.com/datasnaek/youtube-new)

1. Download the data and put in `data/raw`

##  Preprocessing

1. `preprocess/preprocess.py` (no spark, pandas parallel version), `preprocess/preprocess_spark.py` (spark version)
2. data is loaded, selected, joined (category_title), removed null, detect langugage
3. preprocessed data is saved into `data/processed`

Features:
1. video_id
2. title
3. category_id
4. tags
5. views
6. likes
7. dislikes
8. comment_count
9. description
10. category_title
11. region*
12. lang**

\* region: CA, DE, FR, GB, IN, JP, KR, MX, RU, US <br>
** lang: see [wiki](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) for lang code

### result 

---------------------------------------------------------------------------------
| Region_file | Process Time(s) (pandas) | Process Time(s) (spark) | num_record |
|-------------|--------------------------|-------------------------|------------|
|     CA      |           369            |     -                   |    40807   |
|     DE      |           297            |     -                   |    40584   |
|     FR      |           384            |     -                   |    40610   |
|     GB      |           367            |     -                   |    38826   |
|     IN      |           355            |     -                   |    37247   |
|    JP^1     |            56            |     -                   |    20505   |
|   KR^1^2    |            93            |     -                   |    34279   |
|    MX^1     |           533            |     -                   |    40197   |
|   RU^1^2    |           357            |     -                   |    39183   |
|     US      |           361            |     -                   |    40949   |
|   Total     |          3172            |     -                   |   373187   |
---------------------------------------------------------------------------------

^1 The files are not fully written in utf-8 and cannot be decoded normally, the corrupted bytes are removed (by scanning the file byte by bytes) <br>
^2 The files have corrupted records that some description contains non-escaped \n in the description, making the record span in a number of rows. These rows and removed (by scanning the file line by line)

### Corrupted Files

----------------------------------------------------------------------------------------------------------
| Region_file | Process Time(s) (pandas) | Process Time(s) (spark) | num_byte removed | num_line removed |
|-------------|--------------------------|-------------------------|------------------|------------------|
|     JP      |                          |                         |        9         |        0         |
|     KR      |                          |                         |       66         |        1         |
|     MX      |                          |                         |        3         |        0         |
|     RU      |                          |                         |       43         |        9         |
----------------------------------------------------------------------------------------------------------

## EDA


## NLP


## MLlib 