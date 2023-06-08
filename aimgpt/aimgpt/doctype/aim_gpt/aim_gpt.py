# Copyright (c) 2023, Xurpas Inc. and contributors
# For license information, please see license.txt

import frappe,os,json
from langchain.llms import OpenAI
#from llama_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from llama_index import StorageContext, load_index_from_storage
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
    print(f'OPENAI KEY={key}')


@frappe.whitelist()
def ask_question(msg,jsonStr):
    prompt="""You are tasked to give information about AIM's learning programs. 
    		Only answer questions about the courses and learning programs. Answer unrelated questions with "Sorry, I can only answer questions about our learning programs."   
            Only give answers from the provided documents.
            The Question is:
            """
    prompt = prompt+msg 
    jsonDict=json.loads(jsonStr)
    index_file = "../apps/aimgpt/aimgpt/private/index.json"
    print(f'INDEX FILE={index_file}')
    storage_context = StorageContext.from_defaults(persist_dir='../apps/aimgpt/aimgpt/private/')
    #index = GPTVectorStoreIndex.load_from_disk('/home/andy/frappe-bench/apps/aimgpt/aimgpt/private/')
    index = load_index_from_storage(storage_context)
    api_key()
    response = index.as_query_engine().query(prompt)
    jsonDict.append((msg,response.response))
    return jsonDict


