# WunderPy

*A tool to fetch dashboard data from WunderGround*

## Requirements
```
$ pip install bs4
```


## Usage
Typing `wunder -h` in the terminal should result in this output
```
python wunder.py -h
Usage: wunder.py [options]

Options:
  -h, --help            show this help message and exit
  -p, --print           print fetched data
  -i STATION_ID, --id=STATION_ID
                        id of the station
  -o OUTPUT_FILE, --output=OUTPUT_FILE
                        output file (not yet implemented)
```

For example calling with argv `wunder.py -p -i IPDPADOV3` it gives:
```
wind_gust_speed: 41.8 km/h
temperature: 18.5 °C
dewpoint: 17.8 °C
station_id: IPDPADOV3
humidity: 94 %
pressure: 1010 hPa
precip_today: 46 mm
feelslike: 18.5 °C
precip_rate: 0.0 mm/hr
wind_dir: NNW
```

## TODO
-implement output to file

## License
[Apache License](http://www.apache.org/licenses/LICENSE-2.0) Version 2.0, January 2004
