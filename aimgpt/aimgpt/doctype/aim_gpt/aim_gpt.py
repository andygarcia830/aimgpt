# Copyright (c) 2023, Xurpas Inc. and contributors
# For license information, please see license.txt

import frappe,os,json
from langchain.llms import OpenAI
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from frappe.model.document import Document

class AIMGPT(Document):
	pass

def api_key():
    try:
        if (os.environ["OPENAI_API_KEY"] == None or os.environ["OPENAI_API_KEY"] == ''):
            os.environ["OPENAI_API_KEY"] = frappe.get_doc('OpenAI Settings').openai_api_key
            
    except:
        os.environ["OPENAI_API_KEY"] = frappe.get_doc('OpenAI Settings').openai_api_key


    
    key=os.environ["OPENAI_API_KEY"]
    #print(f'OPENAI KEY={key}')


@frappe.whitelist()
def ask_question(msg,jsonStr):
    api_key()
    jsonDict=json.loads(jsonStr)
    index_file = "../apps/aimgpt/aimgpt/private/index.json"
    print(f'INDEX FILE={index_file}')
    index = GPTSimpleVectorIndex.load_from_disk(index_file)
    response = index.query(msg, response_mode="compact")
    jsonDict.append((msg,response.response))
    return jsonDict


