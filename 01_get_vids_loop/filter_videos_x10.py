from java.lang import System
import java.lang.Runtime as Runtime
from burp import IBurpExtender, IHttpListener
import re
import json
import time
import os

current_dir = os.getcwd()

print("Running on Java version: " + System.getProperty("java.version"))


def get_used_vids():
    with open("../01_get_vids_loop/etc/videos_used.txt", "r") as file:
        used_vids = []
        lines = file.readlines()
        for line in lines:
            used_vids.append(line.replace("\n", ""))
            print(line)
        return used_vids


author_id = ""
aweme_id = ""
uid = ""
cid = ""


class BurpExtender(IBurpExtender, IHttpListener):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.registerHttpListener(self)
        callbacks.setExtensionName("filter videos extention")
        callbacks.issueAlert("Hello filter videos alerts!")

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
            # print(error)
            pass

        except Exception as error:
            # print(error)
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

        try:
            if "whatsapp_share_count" in body:
                json_data = json.loads(body)

                if json_data["aweme_list"]:
                    vids = []
                    current_timestamp = time.time()

                    for vid in json_data["aweme_list"]:

                        # -- vid["statistics"] --
                        # "comment_count": 188,
                        # "whatsapp_share_count": 12,
                        # "lose_comment_count": 0,
                        # "repost_count": 0,
                        # "forward_count": 0,
                        # "play_count": 201762,
                        # "lose_count": 0,
                        # "collect_count": 8114,
                        # "download_count": 956,
                        # "share_count": 3732,
                        # "aweme_id": "7447750344307707158",
                        # "digg_count": 59407

                        share_url = vid["share_url"].split("?")[0]
                        create_time = (current_timestamp - vid["create_time"]) / 3600
                        comment_count = vid["statistics"]["comment_count"]
                        digg_count = vid["statistics"]["digg_count"]
                        # unique_id = vid["unique_id"]

                        used_vids = get_used_vids()

                        vids.append(
                            {
                                "share_url": share_url,
                                "create_time": create_time,
                                "comment_count": comment_count,
                                "digg_count": digg_count,
                            }
                        )

                    with open("./res.json", "w") as file:

                        file.write(json.dumps(vids))

        except Exception as error:
            print(error)
            pass

        return headers, body

    def processHttpMessage(self, toolFlag, messageIsRequest, message):
        if messageIsRequest:
            req_headers, req_body = self.getRequestHeadersAndBody(message)
            return

        res_headers, res_body = self.getResponseHeadersAndBody(message)

        # modify block videos
        res_body = res_body.replace("play_addr", "dont_play_addr")
        res_body = res_body.replace("url_list", "dont_url_list")
        new_res = self._helpers.buildHttpMessage(res_headers, res_body)
        message.setResponse(new_res)

        global author_id, aweme_id, uid, cid
        if author_id and aweme_id and uid and cid:

            url = "https://www.tiktok.com/@{}/video/{}?comment_author_id={}&share_comment_id={}".format(
                author_id, aweme_id, uid, cid
            )
            print(url)

            url_exists = False
            with open("./etc/comment_url.txt", "r") as file:
                for line in file:
                    if line.strip() == url:
                        url_exists = True
                        print("url exists")
                        break

            if not url_exists:
                with open("./etc/comment_url.txt", "a") as file:
                    file.write("{}\n".format(url))

            author_id = ""
            aweme_id = ""
            uid = ""
            cid = ""
