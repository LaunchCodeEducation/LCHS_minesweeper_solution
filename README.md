# LCHS_minesweeper

This solution code corresponds to the text and videos in the **Build a Minesweeper Game** chapter from the [LCHS textbook](https://education.launchcode.org/lchs/index.html).

## Flask Setup

After cloning this repo, users will need to create a virtual environment, activate it, and then install Flask. Use a command line interface to navigate into the project folder, then enter the following commands.

*Mac*
```
python3 -m venv game-env
. game-env/bin/activate
pip3 install Flask
```

*Windows (GitBash)*
```
py -3 -m venv game-env
. game-env/Scripts/activate
pip install Flask
```

## Database Setup

In the same directory, run the command `python3 db_setup.py`. This will create the `game.db` database and add the required tables.

## Note

This chapter is under development. When deployed, access its table of contents here: https://education.launchcode.org/lchs/chapters/databases-part2/index.html
