Coingecko Candy Jar
A script that allows you to claim your daily reward from Coingecko.

Requirements
playwright
dotenv
logging
Usage
Clone the repository
Create a .env file in the root of the project and add your environment variables in the following format:
Copy code
u1=username1
p1=password1
u2=username2
p2=password2
Run the script using python
Functionality
The script will check if the daily reward is available and will claim it if it is. Otherwise, it will log a message to inform you that the reward has already been claimed.
If the script failed to claim the reward due to an error, it will retry the claim only once and if it still fails, it will move to the next account and retry the claim the next time you run the script.

Logging
The script uses the logging module to log the different steps and errors that may occur, providing detailed information about the progress and any issues that arise.

Retry Mechanism
The script keeps track of the accounts that failed to claim the reward in a list and retries them the next time the script runs.

Contributing
If you want to contribute to this project, feel free to submit pull requests.

License
This project is licensed under the MIT License.

Disclaimer
This script is for educational purposes only. Use it at your own risk.

Note
This script is designed to be run periodically, with the retry mechanism in place, so that the next time the script runs it will retry the accounts that failed the last time.