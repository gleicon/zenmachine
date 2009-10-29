from twisted.web import server, resource, http
import message, simplejson
# code from: http://zenmachine.wordpress.com/web-services-and-twisted/

class RootResource(resource.Resource):
    def __init__(self, messageStore):
        self.messageStore = messageStore
        resource.Resource.__init__(self)
        self.putChild('check', CheckMessageHandler(self.messageStore))
        self.putChild('train', TrainHandler(self.messageStore))
        self.putChild('delete', RemoveMessageHandler(self.messageStore))                      
        self.putChild('list', ListMessageHandler(self.messageStore))                      

    def getChild(self, path, request):
        return ShowMessage(self.messageStore, "")

class CheckMessageHandler(resource.Resource):
    def __init__(self, messageStore):
        self.messageStore = messageStore
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        return ShowMessage(self.messageStore, path)

class TrainHandler(resource.Resource):
    def __init__(self, messageStore):
        self.messageStore = messageStore
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        return EmptyChild(path)
    
    def render_GET(self, request):
	request.setResponseCode(http.NOT_FOUND)
	return """
		<html><body>use post method for direct insertion or form below<br>
		<form action='/train' method=POST>
		HashKey: <input type=text name=hashKey><br>
		<textarea name=body>Body</textarea><br>
		<input type=submit>
		</body></html>
	"""
    
    def render_POST(self, request):
	hashKey=request.args['hashKey'][0]
	body=request.args['body'][0]
	self.messageStore.setMessage(hashKey,body)
	return "Posted"

class RemoveMessageHandler(resource.Resource):
    def __init__(self, messageStore):
        self.messageStore = messageStore
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        return DelMessage(self.messageStore, path)

class DelMessage(resource.Resource):
    def __init__(self, messageStore, path):
	self.path=path
        self.messageStore = messageStore
        resource.Resource.__init__(self)

    def getChild(self, path, request):
        return EmptyChild(path)
    
    def render_GET(self, request):
	if self.messageStore.hasMessage(self.path):
		self.messageStore.delMessage(self.path)
       		return """ msg %s deleted	""" % (self.path)
       	else:
		return """ msg not found for hashKey: %s""" % self.path

class EmptyChild(resource.Resource):
    def __init__(self, path):
        self.path = path
        resource.Resource.__init__(self)

    def render_GET(self, request):
	return ""
    
    def render_POST(self, request):
	return ""

    def getChild(self, path, request):
        return EmptyChild(path)


class ListMessageHandler(resource.Resource):
    def __init__(self, messageStore):
        self.messageStore = messageStore
        resource.Resource.__init__(self)
	
    def render_GET(self, request):
	msgList=self.messageStore.listMessages()
	if len(msgList) > 0:
		#return str(msgList)
		return simplejson.dumps(msgList)
       	else:
		return """empty messageStore"""

    def getChild(self, path, request):
        return EmptyChild(path)


class ShowMessage(resource.Resource):
    def __init__(self, messageStore, path):
        self.messageStore = messageStore
	self.path = path
        resource.Resource.__init__(self)
	
    def render_GET(self, request):
	if self.messageStore.hasMessage(self.path):
            	hashKey=self.path
		msg=self.messageStore.getMessage(self.path)
		return simplejson.dumps([hashKey, msg])
       	else:
		return """msg not found for hashKey: %s""" % self.path

    def getChild(self, path, request):
        return EmptyChild(path)

if __name__ == "__main__":
    import sys
    from twisted.internet import reactor
    messageStore = message.MessageStore(sys.argv[1])
    reactor.listenTCP(8082, server.Site(RootResource(messageStore)))
    reactor.run()
