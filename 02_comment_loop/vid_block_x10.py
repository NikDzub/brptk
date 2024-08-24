from java.lang import System
import java.lang.Runtime as Runtime
from burp import IBurpExtender, IHttpListener
import re
import json

# mime_type=video_mp4

print("Running on Java version: " + System.getProperty("java.version"))


class BurpExtender(IBurpExtender, IHttpListener):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        callbacks.setExtensionName("Video block")
        callbacks.issueAlert("Hello alerts!")

    def getResponseHeadersAndBody(self, content):
        response = content.getResponse()
        response_data = self._helpers.analyzeResponse(response)
        headers = list(response_data.getHeaders())
        body = response[response_data.getBodyOffset() :].tostring()
        print(headers)
        return headers, body

    def processHttpMessage(self, toolFlag, messageIsRequest, content):
        if messageIsRequest:
            return

        res_headers, res_body = self.getResponseHeadersAndBody(content)

        print(type(res_body))
        print(res_body)

        # modify
        res_body = res_body.replace("play_addr", "dont_play_addr")
        new_res = self._helpers.buildHttpMessage(res_headers, res_body)
        content.setResponse(new_res)
