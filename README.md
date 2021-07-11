# PowerBot 

This is Default Discord Bot

Features :
Game
Kick and Ban
Music(Next Releases)
Embed
and More . . .


## How to download it

* Create a Discord bot [here](https://discord.com/developers/applications)
* Get your bot token
* Invite your bot on servers using the following invite:
  https://discordapp.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID&scope=bot&permissions=8 (
  Replace `YOUR_APPLICATION_ID` with the application ID)

## How to Set up

To set up the bot I made it as simple as possible. I now created a [config.json](config.json) file where you can put the
needed things to edit.

| Variable                  | What it is                                                            |
| ------------------------- | ----------------------------------------------------------------------|
| PREFIX                   | The Prefix(es) of your bot                                            |
| TOKEN                  | The token of your bot                                                 |
| APPLICATION_ID  | The application ID of your bot                                        |
| OWNERS               | The user ID of all the bot owners                                     |

In the [blacklist](blacklist.json) file you now can add IDs (as integers) in the `ids` list.

## How to start

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows), or your CMD or Terminal

```
python bot.py
```

## Requirement

```
pip install discord.py
```
or
```
sudo apt-get install discord.py 
```

## License

This project is licensed under the MIT License 2.0 - see the [LICENSE.md](LICENSE.md)
