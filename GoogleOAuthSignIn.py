from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import gdata


class GoogleOAuthSignIn():

    def __init__(self):
        pass

    SCOPE = ['http://www.google.com/m8/feeds/contacts/']

    @staticmethod
    def connect():
        flow = flow_from_clientsecrets(
            filename='config/client_secret.json',
            scope=GoogleOAuthSignIn.SCOPE,
            message='Please create a project in the Google Developer Console and place the client_secret.json '
                    'authorization file along this script'
        )
        storage = Storage('config/credentials.json')
        credentials = storage.get()
        if credentials is None:
            credentials = tools.run_flow(flow, storage, tools.argparser.parse_args([]))
        # GData with access token
        token = gdata.gauth.OAuth2Token(
            client_id=flow.client_id,
            client_secret=flow.client_secret,
            scope=GoogleOAuthSignIn.SCOPE,
            user_agent=flow.user_agent,
            access_token=credentials.access_token,
            refresh_token=credentials.refresh_token)

        # Construct the Contacts service and authenticate
        contacts_client = gdata.contacts.client.ContactsClient(auth_token=token)
        token.authorize(contacts_client)
        return contacts_client