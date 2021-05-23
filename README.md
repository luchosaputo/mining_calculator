# Mining Calculator

Mining Calculator is a Python program that checks nicehash mining profitability.

## Usage
First make sure to set the config correctly, editing the `config.ini` file. 

**You should setup:**
- `graphicsCard` to your graphics card model (must match niceHash)
- either `mineUsdPerDay` or `minBtcPerDay` **NOT** both
- `timeInterval` determines how often the program will run

```cmd
pip install -r requirements.txt
python '.\ main.py'  
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
