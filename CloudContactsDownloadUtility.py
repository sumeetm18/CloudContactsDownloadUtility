#!/usr/bin/env python
from GoogleOAuthSignIn import GoogleOAuthSignIn
import abc
import gdata.contacts.client
import gdata.contacts.data
import gdata.data
import re
import time


class CloudContactManager():
    '''
    Abstract Class to connect and do the operation on different contact storage utls
    '''
    __metaclass__  = abc.ABCMeta

    def getallcontacts(self):
        raise NotImplementedError()

    def writecontactstocsv(self):
        raise NotImplementedError()


class MicrsoftContactManager(CloudContactManager):
    pass


class GoogleContactsManager(CloudContactManager):

    def __init__(self, contacts_client):
        """Creates a contact manager for the contact list of a user.
        Args:
          contacts_client: The gdata.contacts.client.ContactsService instance to
            use to perform GData calls.
        """
        self.contacts_client = contacts_client

    def writecontactstocsv(self , contact_entries):
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
    contacts_client = GoogleOAuthSignIn.connect()
    contacts_manager = GoogleContactsManager(contacts_client)
    contact_entries = contacts_manager.getallcontacts()
    contacts_manager.writecontactstocsv(contact_entries)


if __name__ == '__main__':
    main()