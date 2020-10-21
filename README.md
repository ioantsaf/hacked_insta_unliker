# Hacked Insta Unliker

## Python script to detect and remove suspicious likes from Instagram

Created mainly for the victims of the [Nano Defender/AdBlocker malware](https://github.com/jspenguin2017/Snippets/issues/3)

Uses the [instagram_private_api](https://github.com/ping/instagram_private_api) library to access Instagram

## Installation

Python 3.6+ is required
```
pip install -r requirements.txt
```

## Usage

### Configuration

The file `config.json.example` can optionally be copied to `config.json`, to define your username and password and change some default values:
- `username`: Your Instagram username. Can also be entered when the script runs.
- `password`: Your Instagram username. Can also be entered when the script runs.
- `date_threshold_str`: The date after which your likes are being scanned
- `s_min`: The minimum time in seconds to wait before removing a like
- `s_max`: The maximum time in seconds to wait before removing a like

The values `s_min` and `s_max` are used to avoid rate limiting. If you want the script to run fast, you can set both values to 0.
Your account may receive a temporary lock, if you have many likes to remove.

When you enter your credentials while the script runs, they are only used once and will not be saved.

### Execution

```
python unliker.py
```

The script scans for likes to users you do not follow, for posts after 1/9/2020 (the threshold can be configured in the parameter `date_threshold_str` in `config.json`).  
It then shows the suspicious likes' users, and offers the option to exclude some users from removing likes to.  
Finally, when you choose to proceed, all non-excluded suspicious likes are removed.
