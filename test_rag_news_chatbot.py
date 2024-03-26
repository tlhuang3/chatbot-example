from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

print("Loading documents")
# Loading documents from local disk
loader = DirectoryLoader('./', glob="nvidia_news_0309.txt", show_progress=True)
documents = loader.load()

# Split documents into chunks
# Checked with ChunkViz to confirm chunk_size with 500 contains (everything within a pair of parentheses in one chunk)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
chunks = text_splitter.split_documents(documents)

print("Creating embeddings")
# Create embeddings for each chunk
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever()

print("Creating chains")
llm = ChatOpenAI()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = ConversationalRetrievalChain.from_llm(
    llm, retriever=retriever, memory=memory, verbose=True)

while(True):
    user_input = input("> What do you want to know about Nvidia? ")
    result = conversation.invoke(user_input)
    print(result["answer"])