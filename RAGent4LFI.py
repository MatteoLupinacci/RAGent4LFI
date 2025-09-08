import os
import random
import string
import requests
import re

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool
from langchain_community.document_loaders import PyMuPDFLoader

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = ""

#============================================ RAG settings ============================================

#setup the loader and load the documents (or directly the page_content (text))
documents_page_list = []
pdf_folder = "owasp_pdf"
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        print(filename)
        file_path = os.path.join(pdf_folder, filename)
        loader = PyMuPDFLoader(file_path)
        documents_page_list.extend(loader.load())
print(f"Number of loaded pdf pages:", len(documents_page_list))

#setup the splitter and split the documents in chunks
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000,  chunk_overlap=200,  add_start_index=True)
chunks = splitter.split_documents(documents_page_list)

#setup the embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

#setup the vectore store based on the embeddings model
vector_store = InMemoryVectorStore(embeddings)

#store chunks in a vectorstore
stored_chunks = vector_store.add_documents(chunks)


#============================================ LLM Tools settings ============================================
api_base_url = "http://localhost:5000" # URL to the kali server for running commands

@tool
def retrieval(query):
  """Retrieve information related to a query."""
  retrieved_chunks = vector_store.similarity_search(query,k=4) #by default, select k=4 more relavant documents.
  ret = "\n\n".join(
        (f"Source: {chunk.metadata}\n" f"Content: {chunk.page_content}")
        for chunk in retrieved_chunks
  )
  return ret

@tool
def test_url_for_lfi(target_url):
    """Try to test a given URL for LFI using well known payload."""
    responses = []

    paths = find_path_with_gobuster(target_url)
    retrieved_text = retrieval.invoke("find typical PAYLOAD for LFI vuln")
    payloads = re.findall(r"(?<!\w)(?:\.\./|/)(?:\.\./)*[\w./-]+(?=\s|$)", retrieved_text)

    for path in paths:
      url_with_path = target_url + path
      query_params, payload = find_query_params_with_wfuzz(url_with_path,payloads)
      vulnerable = len(query_params) > 0
      print(f"URL seems vulnerable: {vulnerable}")

      if vulnerable:
        test_url = url_with_path + "?" + query_params[0] + "=" + payload
        try:
          response = requests.get(test_url, timeout=5)
          responses.append(f"Tested: {test_url} -> HTTP {response.status_code}")
          if "root:x:0:0:" in response.text:
              responses.append(f"❗ ATTENTION ❗ --> LFI found for {test_url}")
              vulnerable = True
              break
        except requests.RequestException:
            responses.append(f"Error during LFI test request: {test_url}")

    return "\n".join(responses) if vulnerable else "No LFI vuln found."

@tool
def execute_command(command):
    """Execute a command in the terminal of a remote machine."""
    api_url = api_base_url+"execute_command"
    response = requests.post(api_url, json={"command": command})
    output = response.json()["output"]
    return output

# setup tool list
tools = []
tools.append(retrieval)
tools.append(test_url_for_lfi)
tools.append(execute_command)

# helper method used by tool
def find_path_with_gobuster(target):
    """Execute gobuster dir scan for finding web paths in the terminal."""
    api_url = api_base_url+"find_path_with_gobuster"
    response = requests.post(api_url, json={"target_url": target})

    if response.status_code == 200:
      paths_found = response.json()["paths"]
      if len(paths_found) == 0:
        return f"No paths found."
      return paths_found
    else:
      return f"Error during API call: {response.text}"

def find_query_params_with_wfuzz(target,payloads):
    """Execute wfuzz scan for finding query params of web paths in the terminal."""
    api_url = api_base_url+"find_query_params_with_wfuzz"

    for payload in payloads:
      response = requests.post(api_url, json={"target_url": target, "payload":payload})
      if response.status_code == 200:
        query_params_found = response.json()["params"]
        if len(query_params_found) > 0:
          return query_params_found, payload #found at least 1 working payload

    return [], None #no working payload found


#============================================ Agentic RAG settings ============================================
# set the LLM model
model = init_chat_model("gpt-4o-mini", model_provider="openai")
system_promt = "You are a technical assistant specialized in cybersecurity and vulnerabilities assessment. Users ask you to analyze a given URL and test it against Local File Inclusion vulnerabilities. Use all the tools you need. If you realize that the URL is vulnerable, STOP EVERYTHING and return: URL VULN TO LFI❗❗❗"

#setup memory agent capacity
memory = MemorySaver()

# create the agent using langgraph
rag_agent = create_react_agent(model, tools, prompt=system_promt, checkpointer=memory)

# setup the configuration of the thread used for this conversation with the agent
random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
config = {"configurable": {"thread_id": random_string}}

def main():
  print("\n🤖 How can I help you today? 💡", end = "")
  message = input()
  inputs = {"messages": [("user", message)]}
  for stream in rag_agent.stream(inputs, stream_mode="values",config=config):
    stream["messages"][-1].pretty_print()

if __name__ == '__main__':
  main()