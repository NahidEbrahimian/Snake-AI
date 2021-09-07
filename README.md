# Snake AI

**Rule based snake**

https://user-images.githubusercontent.com/82975802/132351422-042cf725-3163-427f-9753-07fc3b86b2bc.mp4


## Train

1- First you must generate training data using the following command:

num_generate_rows --> number of rows in csv file(training sampels)

dataset --> file_name.csv

```
!python3 generate_data.py --num_generate_rows 500000 --dataset Dataset.csv
```

2- Train model:

```
!python3 model.py
```

## Test

Run the following command to test trained model:

model --> path of trained model

```
!python3 machine_learning.py --model Train/model.h5
```
