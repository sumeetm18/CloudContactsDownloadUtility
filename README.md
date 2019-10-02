A script to download the contacts from cloud.

# Contents

Python script for downloading the  contacts: CloudContactsDownloadUtility.py



# Installation

```
pip install -r requirements.txt
```

# Setup

1. Create a project in the [Google Developers Console](https://console.developers.google.com)
2. Enable the Contacts API
3. Create an OAuth client ID credential
4. Save the json file as ```client_secret.json```  in config folder.


# Requirements

- Python 2.7

- oauth2client available at:  
  https://github.com/google/oauth2client

- GData Python client library available at:  
  https://github.com/google/gdata-python-client

# Usage
Exports all contacts of the user to ContactExport.csv in Downloads Folder:
  ```
  python CloudContactsDownloadUtility.py
  ```


# Links

- oauth2client library  
  https://oauth2client.readthedocs.io/en/latest/index.html

- GData Python client library  
  https://developers.google.com/gdata/articles/python_client_lib  
  https://pythonhosted.org/gdata

- Script home page  
  https://github.com/sumeetm18/CloudContactsDownloadUtility


# Upcoming Enhancements

- Option to specify the cloud storage.Currently by default the script works for google contacts.
- Other Operation on Contacts Management like Create,Delete,Update.
- Currently downloaded csv will have only name and number. With later enhancement we will have all the fields populated.
- Better Exceptions handling.
- Support for  python 3 version.