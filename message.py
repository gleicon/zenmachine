import pickle, os, sys
# code from: http://zenmachine.wordpress.com/web-services-and-twisted/


class MessageStore(object):
    "class for managing messages in the form: md5hash:text"
    
    def __init__(self, filename):
        self.filename = filename
        if os.path.exists(filename):
            self.messages = pickle.load(file(filename, 'r+b'))
        else:
            self.messages = {}

    def save(self):
        pickle.dump(self.messages, file(self.filename, 'w+b'))

    def hasMessage(self, hashKey):
        return self.messages.has_key(hashKey)

    def listMessageKeys(self):
        return self.messages.keys()
    
    def listMessages(self):
        return self.messages.items()

    def getMessage(self, hashKey):
        return self.messages[hashKey]

    def setMessage(self, hashKey, content):
        self.messages[hashKey] = content
        self.save()

    def delMessage(self, hashKey):
        del(self.messages[hashKey])

if __name__ == "__main__":
	messages = MessageStore(sys.argv[1])
	messages.setMessage('AAA', "oieee")
	print messages.listMessages()
	print messages.hasMessage('AAA')
	print messages.getMessage('AAA')
	print ["%s=%s" % (h, m) for h,m in messages.listMessages()]
