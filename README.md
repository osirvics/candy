# Coingecko Candy Jar

A Python script that allows you to claim your daily reward from Coingecko.

## Requirements
- [playwright](https://github.com/microsoft/playwright)

## Usage
- Clone the repository
- Create a `.env` file in the root of the project and add your environment variables in the following format:
```
u1=username1
p1=password1
u2=username2
p2=password2
```
- Run the script using python 

## Functionality
The script will check if the daily reward is available and will claim it if it is. Otherwise, it will log a message to inform you that the reward for the specific account was not claimed.
If the script failed to claim the reward due to an error, it will save the index and move to the next account and retry the claim again after other accounts have been claimed succesfully.


## Retry Mechanism
The script keeps track of the accounts that failed to claim the reward in a list and retries them.

## Contributing
If you want to contribute to this project, feel free to submit pull requests.

## License
This project is licensed under the MIT License.

## Disclaimer
This script is for educational purposes only. Use it at your own risk.
