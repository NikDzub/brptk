from burp import IBurpExtender, IHttpListener


class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        callbacks.setExtensionName("Hello Extension")
        print("Hello Burp")
        callbacks.issueAlert("Hello alerts!")

    def getResponseHeadersAndBody(self, content):
        response = content.getResponse()
        response_data = self._helpers.analyzeResponse(response)
        headers = list(response_data.getHeaders())
        body = response[response_data.getBodyOffset() :].tostring()
        return headers, body

    def processHttpMessage(self, tool, is_request, content):
        if is_request:
            return

        headers, body = self.getResponseHeadersAndBody(content)

        # modify body
        body = body.replace('digg_count":0,', 'digg_count":13242340,')

        new_message = self._helpers.buildHttpMessage(headers, body)
        content.setResponse(new_message)
