#!/usr/bin/env python
import abc
import gdata.contacts.client
import gdata.contacts.data
import gdata.data
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import re
import time


class CloudContactManager():
    '''
    Abstract Class to connect and do the operation on different contact storage utls
    '''
    __metaclass__  = abc.ABCMeta

    def getallcontacts(self):
        pass

    def connect(self):
        pass

    def writecontactstocsv(self):
        pass


class GoogleContactsManager(CloudContactManager):

    SCOPE = ['http://www.google.com/m8/feeds/contacts/']

    def __init__(self, contacts_client):
        """Creates a contact manager for the contact list of a user.

        Args:
          contacts_client: The gdata.contacts.client.ContactsService instance to
            use to perform GData calls.
        """
        self.contacts_client = contacts_client

    @classmethod
    def connect(cls):
        flow = flow_from_clientsecrets(
            filename='config/client_secret.json',
            scope=GoogleContactsManager.SCOPE,
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
            scope=GoogleContactsManager.SCOPE,
            user_agent=flow.user_agent,
            access_token=credentials.access_token,
            refresh_token=credentials.refresh_token)

        # Construct the Contacts service and authenticate
        contacts_client = gdata.contacts.client.ContactsClient(auth_token=token)
        token.authorize(contacts_client)
        return contacts_client

    def writecontactstocsv(self,contact_entries):
        """Creates a csv with name and numbers from contact entries passed.
        Args:
        contact_entries: Generator Object of all the gdata.contacts.data.ContactEntries
        """
        rx = re.compile('\W+')
        allcontacts = []
        for entry in contact_entries:
            if entry.name is not None and len(entry.phone_number) > 0 and len(entry.group_membership_info) > 0:

                # Clean up characters in contact name; replace all non-alphanumerics with spaces
                fullname = entry.name.full_name.text
                fullname = rx.sub(' ', fullname).strip()
                for rawPhoneNumber in entry.phone_number:
                    # Remove non-numeric characters from the phone number
                    phone_number = re.sub("[^0-9]", "", rawPhoneNumber.text)
                    # Save contact for later insert
                    allcontacts.append((fullname, phone_number))

        allcontacts = tuple(set(allcontacts))

        csvfilename = "Downloads/ContactExport"+time.strftime("%Y%m%d-%H%M%S")+".csv"
        csvfile = open(csvfilename, "w")
        for csvFullName, csvPhoneNumber in allcontacts:
            line = "\"%s\",%s\n" % (csvFullName, csvPhoneNumber)
            csvfile.write(line)

        csvfile.close()

    def getallcontacts(self):
        """Retrieves all contacts in the contact list.
        Yields:
          gdata.contacts.data.ContactEntry objects.
        """
        feed_url = self.contacts_client.GetFeedUri(projection='full')
        total_read = 0
        while True:
            print('Retrieving contacts... (%d retrieved so far)' % total_read)
            feed = self.contacts_client.get_feed(uri=feed_url,
                                                 auth_token=None,
                                                 desired_class=gdata.contacts.data.ContactsFeed)
            total_read += len(feed.entry)
            for entry in feed.entry:
                yield entry
            next_link = feed.GetNextLink()
            if next_link is None:
                print('All contacts retrieved: %d total' % total_read)
                break
            feed_url = next_link.href


def main():
    contacts_client = GoogleContactsManager.connect()
    contacts_manager = GoogleContactsManager(contacts_client)
    contact_entries = contacts_manager.getallcontacts()
    contacts_manager.writecontactstocsv(contact_entries)


if __name__ == '__main__':
    main()