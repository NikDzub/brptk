from java.lang import System
import java.lang.Runtime as Runtime
from burp import IBurpExtender, IHttpListener
import re
import json

print("Running on Java version: " + System.getProperty("java.version"))

author_id = ""
aweme_id = ""
uid = ""
cid = ""


class BurpExtender(IBurpExtender, IHttpListener):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        callbacks.setExtensionName("My extention")
        callbacks.issueAlert("Hello alerts!")

    def getRequestHeadersAndBody(self, content):
        request = content.getRequest()
        request_data = self._helpers.analyzeRequest(request)
        headers = list(request_data.getHeaders())
        body = request[request_data.getBodyOffset() :].tostring()

        try:
            if "/aweme/v2/comment/list/" in headers[0]:
                global aweme_id, author_id

                aweme_id = re.search(r"aweme_id=(\d+)", str(headers[0])).group(1)
                author_id = re.search(r"author_id=(\d+)", str(headers[0])).group(1)

        except Exception as error:
            print(error)
            pass
        return headers, body

    def getResponseHeadersAndBody(self, content):
        response = content.getResponse()
        response_data = self._helpers.analyzeResponse(response)
        headers = list(response_data.getHeaders())
        body = response[response_data.getBodyOffset() :].tostring()

        try:
            if '"comment":{' in body:
                global cid, uid

                cid = re.search(r'"cid":"(.*?)"', str(body)).group(1)
                uid = re.search(r'"uid":"(.*?)"', str(body)).group(1)

        except Exception as error:
            print(error)
            pass
        return headers, body

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if messageIsRequest:
            req_headers, req_body = self.getRequestHeadersAndBody(message)
            return

        res_headers, res_body = self.getResponseHeadersAndBody(message)

        new_res = self._helpers.buildHttpMessage(res_headers, res_body)
        message.setResponse(new_res)

        global author_id, aweme_id, uid, cid
        if author_id and aweme_id and uid and cid:

            url = "https://www.tiktok.com/@{}/video/{}?comment_author_id={}&share_comment_id={}".format(
                author_id, aweme_id, uid, cid
            )
            print(url)

            with open("./urls.txt", "a") as file:
                file.write("{}\n".format(url))

            author_id = ""
            aweme_id = ""
            uid = ""
            cid = ""
