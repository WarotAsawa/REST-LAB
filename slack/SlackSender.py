import requests
import json

class SlackSender:
  def __init__(self, webhook):
    self.webhook = webhook


  def SendMessage(self, message):
    """Send a Slack message to a channel via a webhook. 
    Returns:
        HTTP response code, i.e. <Response [503]>
    """

    return requests.post(self.webhook, json.dumps({"text": message}))


  def SendBlockImage(self, blockMessage, blockImageURL, imageDes, imageURL):
    block = {}
    image = {}
   
    block["type"] = "section"
    block["text"] = {"type" : "mrkdwn","text" : blockMessage}
    block["accessory"] = {}
    block["accessory"]["type"] = "image"
    block["accessory"]["image_url"] = blockMessage
    block["accessory"]["alt_text"] = blockImageURL
    
    image["type"] = "image"
    image["title"] = {"type": "plain_text","text": imageDes,"emoji": True}
    image["image_url"] = imageURL
    image["alt_text"] = imageDes

    payload = {"blocks":[block,image]}
   
    return requests.post(self.webhook, json.dumps(payload))

