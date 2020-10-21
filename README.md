# Hacked Insta Unliker

## Python script to detect and remove suspicious likes from Instagram

Created mainly for the victims of the [Nano Defender/AdBlocker malware](https://github.com/jspenguin2017/Snippets/issues/3)

Uses the [instagram_private_api](https://github.com/ping/instagram_private_api) library to access Instagram

## Installation

```
pip install -r requirements.txt
```

## Usage

Either provide the username and password by creating a `config.json` file with the structure of `config.json.example`, or enter the username and password while running the script.
Your credentials will only be used once and will not be saved.

```
python unliker.py
```

The script scans for likes to users you do not follow, for posts after 1/9/2020 (the threshold can be configured in the parameter `date_threshold_str` in `config.json`).  
It then shows the suspicious likes' users, and offers the option to exclude some users from removing likes to.  
Finally, when you choose to proceed, all non-excluded suspicious likes are removed.
