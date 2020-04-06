# Shot Boundary

A shot boundary can be categorized into cuts and gradual transitions [1].

```
Input: Video
Output: 2 type: + Gradual transition : starting frame - ending frame
                + Cut : staring frame
```
This code support 3 dataset: BBC EastEnders, [TVsum50](https://github.com/yalesong/tvsum), [SumMe](https://gyglim.github.io/me/vsum/index.html).

## Usage code

```bash
python Main_SBD.py name-dataset
```
name-dataset = [bbc, tvsum, summe] 

To use another dataset, change dir of 2 variable ```data_path, output_path```

#### Output of this code
The information of each shot is written in a file with the following format
```
<start time of shot> <end time of shot> <score of shot>
HH:MM:SS.FFFF HH:MM:SS.FFFF float (1st shot)
HH:MM:SS.FFFF HH:MM:SS.FFFF float (2nd shot)
...
HH:MM:SS.FFFF HH:MM:SS.FFFF float (nth shot)
```

