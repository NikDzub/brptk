from java.lang import System  # Java import
from burp import IBurpExtender, IHttpListener

print("Running on Java version: " + System.getProperty("java.version"))


class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        callbacks.setExtensionName("test_01")
        callbacks.issueAlert("Hello alerts!")

    def getResponseHeadersAndBody(self, content):
        response = content.getResponse()
        response_data = self._helpers.analyzeResponse(response)
        headers = list(response_data.getHeaders())
        body = response[response_data.getBodyOffset() :].tostring()

        # print(f"response - ")
        return headers, body

    def getRequestHeadersAndBody(self, content):
        request = content.getRequest()
        request_data = self._helpers.analyzeRequest(request)
        headers = list(request_data.getHeaders())
        body = request[request_data.getBodyOffset() :].tostring()

        # print(f"request - ")
        if "/aweme/v2/comment/list/" in headers[0]:
            print("comment")

        return headers, body

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if messageIsRequest:
            headers, body = self.getRequestHeadersAndBody(message)
            return

        res_headers, res_body = self.getResponseHeadersAndBody(message)

        print(res_body)

        # res_body = res_body.replace("resolution=320*439,", "resolution=120*139")

        new_res = self._helpers.buildHttpMessage(res_headers, res_body)
        message.setResponse(new_res)
