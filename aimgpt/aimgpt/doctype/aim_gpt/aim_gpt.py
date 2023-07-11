# Copyright (c) 2023, Xurpas Inc. and contributors
# For license information, please see license.txt

import frappe,os,json,openai
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
    openai.api_key=key
    print(f'OPENAI KEY={key}')


@frappe.whitelist()
def ask_question(msg,jsonStr):
    print(f'JSON={jsonStr}')
    settings = frappe.get_doc('AIM GPT Settings')
    prompt = settings.guardrails
    if prompt == None:
         prompt = ""
    prompt=prompt +"""
    The Question is:
    """
    prompt = prompt+msg 
    print(prompt)
    jsonDict=json.loads(jsonStr)
    index_file = "../apps/aimgpt/aimgpt/private/index.json"
    print(f'INDEX FILE={index_file}')
    api_key()
    storage_context = StorageContext.from_defaults(persist_dir='../apps/aimgpt/aimgpt/private/')
    #index = GPTVectorStoreIndex.load_from_disk('/home/andy/frappe-bench/apps/aimgpt/aimgpt/private/')
    index = load_index_from_storage(storage_context)

    response = index.as_query_engine().query(prompt)
    jsonDict.append((msg,response.response.strip('\n')))
    return jsonDict



@frappe.whitelist()
def fetch_sample_questions():
    settings = frappe.get_doc('AIM GPT Settings')
    #questions = frappe.get_doc('AIM GPT Sample Questions',settings.sample_questions)
    questions = settings.sample_questions
    print(f'QUESTIONS={questions}')
    result=[]
    for item in questions:
          result.append(item.question)
    ip = frappe.get_request_header('X-Forwarded-For')
    print(f'REQUEST={ip}')
    return result