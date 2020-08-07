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
seperator = "<\\ if running on windows, / everywhere else>"
```

### Dependencies:

#### Pip:
discordpy<br>
pafy<br>
youtube_dl<br>

#### Applications:
ffmpeg<br>
