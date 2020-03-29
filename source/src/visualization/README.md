# How to run the visual tool for video summarization
This tool used the [amalia.js](https://ina-foss.github.io/amalia.js/) source

### Framework
```
Flask==1.1.1
```
Using the following command to run a visual website
```python
python demo.py
```

All the information for visualization is saved as json file in *static/json*.
* Json file format for shot visualization
```
{
    "localisation": [
        {
            "sublocalisations": {
                "localisation": [
                    {
                        "label": "4.5",
                        "tc": "00:00:01.6800",
                        "tclevel": 1
                    },
                    {
                        "label": "3.7",
                        "tc": "00:00:03.3600",
                        "tclevel": 1
                    },

                ]
            },
            "type": "events",
            "tcin": "00:00:00.0000",
            "tcout": "00:00:15.0000",
            "tclevel": 0
        }
    ],
    "id": "shot_id",
    "type": "events",
    "algorithm": "demo-video-generator",
    "processor": "",
    "processed": 0,
    "version": 1
}
```

* Json file format for segment visualization
{
    "localisation": [
        {
            "sublocalisations": {
                "localisation": [
                    {
                        "tcin": "00:00:01.6800",
                        "tcout": "00:00:03.3600",
                        "tclevel": 1
                    },
                    {
                        "tcin": "00:00:05.0400",
                        "tcout": "00:00:06.7200",
                        "tclevel": 1
                    },

                ]
            },
            "type": "segments",
            "tcin": "00:00:00.0000",
            "tcout": "00:00:15.0000",
            "tclevel": 0
        }
    ],
    "id": "seg_id",
    "type": "segments",
    "algorithm": "demo-video-generator",
    "processor": "",
    "processed": 0,
    "version": 1
}
