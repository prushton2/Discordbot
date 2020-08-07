# Discordbot

### Files in gitignore:

Create these files before running

Config.json: 
```javascript
{
  "prefix":"<Desired prefix goes here>",
  "token":"<Paste bot token here>"
}
```

userData.json:
```javascript
{"users": {} }
```

pyconfig.py:

```python
userDataPath = "<Path to userdata.json>"
configPath = "<Path to config.json>"
songsPath = "<Path to a folder to hold songs>"
```

### Dependencies:

discordpy
pafy
ffmpeg