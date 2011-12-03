from twilio.rest import TwilioRestClient

class SMS:

    class FriendlySMSFacade:
        def __init__(self, sms):
            self.body=sms.body
            self.from_=sms.from_

        def get_body(self):
            return self.body

        def get_source(self):
            return self.from_

    def __init__(self):
        account = "ACf3a4c18fb6b24d01a99aa2770c187900"
        token = "d83d9fb72dd8a2fbe04c112ec6fe2577"
        self.client = TwilioRestClient(account, token)

    used_messages=[]

    @classmethod
    def is_used(cls, msg):
        return msg.sid in cls.used_messages

    @classmethod
    def mark_as_used(cls, msg):
        if not cls.is_used(msg):
            print msg.sid+"is now used"
            cls.used_messages.append(msg.sid)
            

    def send(self, message, number):
        """ true if sending is successful"""
        msg = self.client.sms.messages.create(to=number, from_="+14155992671",
                body=message+"\n to reply type 5370-3238 before your message")

        return msg.status == "sent" or msg.status == "pending"

    def receive(self):
        """ List of not yet seen responses """
        all_messages=self.client.sms.messages.list()

        to_return=[]

        #go through all the messages
        for msg in all_messages:

            if msg.status == "received" and (not SMS.is_used(msg)):
                to_return.append(SMS.FriendlySMSFacade(msg))
                SMS.mark_as_used(msg)

        return to_return