# Urban Mobility Backend System

A console-based application to securely manage a system of admins, service engineers, travelers and scooters.

## Running
To run the program, first create a Python virtual environment
```shell
python -m venv .venv/
```
Then activate the virtual environment
### Windows
```shell
.venv\Scripts\activate.bat
```
### Linux
```shell
source .venv/bin/activate
```
Then install the required packages
```shell
pip install -r requirements.txt
```
Then run the program
```shell
python app/main.py
```

## Feature checklist
### Service Engineer
- [ ] To update their own password
- [ ] To update some attributes of scooters in the system
- [ ] To search and retrieve the information of a scooter
### System Administrator
- [ ] To update their own password
- [ ] To update some attributes of scooters in the system
- [ ] To search and retrieve the information of a scooter
- [x] To check the list of users and their roles
- [x] To add a new Service Engineer to the system
- [x] To update an existing Service Engineer account and profile
- [x] To delete an existing Service Engineer account
- [ ] To reset an existing Service Engineer password (a temporary password)
- [ ] To update his own account and profile
- [ ] To delete his own account
- [ ] To make a backup of the backend system
- [ ] To restore a specific backup of the backend system. For this purpose, the Super Administrator has generated a specific ‘one-use only’ code to restore a specific backup
- [x] To see the logs file(s) of the backend system
- [ ] To add a new Traveller to the backend system
- [ ] To update the information of a Traveller in the backend system
- [ ] To delete a Traveller record from the backend system
- [x] To add a new scooter to the backend system
- [x] To update the information of a scooter in the backend system
- [x] To delete a scooter from the backend system
- [ ] To search and retrieve the information of a Traveller
### Super administrator
- [ ] To update the attributes of scooters in the system
- [ ] To search and retrieve the information of a scooter
- [x] To check the list of users and their roles
- [x] To add a new Service Engineer to the backend system
- [x] To modify or update an existing Service Engineer account and profile
- [x] To delete an existing Service Engineer account
- [ ] To reset an existing Service Engineer password (a temporary password)
- [x] To see the logs file(s) of the backend system
- [ ] To add a new Traveller to the backend system
- [ ] To update the information of a Traveller in the backend system
- [ ] To delete a Traveller from the backend system
- [x] To add a new scooter to the backend system
- [x] To update the information of a scooter in the backend system
- [x] To delete a scooter from the backend system
- [ ] To search and retrieve the information of a Traveller
- [x] To add a new System Administrator to the backend system
- [x] To modify or update an existing System Administrator account and profile
- [x] To delete an existing System Administrator account
- [ ] To reset an existing System Administrator password (a temporary password)
- [ ] To make a backup of the backend system and to restore a backup
- [ ] To allow a specific System Administrator to restore a specific backup. For this purpose, the Super Administrator should be able to generate a restore-code linked to a specific backup and System Administrator. The restore-code is one-use-only
- [ ] To revoke a previously generated restore-code for a System Administrator
