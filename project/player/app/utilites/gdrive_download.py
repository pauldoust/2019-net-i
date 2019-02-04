import requests

def writeToFile(response, filePath):
    CHUNK = 1024
    with open(filePath, "wb") as f:
        for chunk in response.iter_content(CHUNK):
            if chunk:
                f.write(chunk)

def downloadShareableLinkById(fileId, filePath):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : fileId }, stream = True)
    token = None
    for k, v in response.cookies.items():
        if k.startswith('download_warning'):
            token = v

    if token:
        params = { 'id' : fileId, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    writeToFile(response, filePath)    




# fileId = '1FbGFApkcR5ZQ_4rLFgm4U8YdIzOvuYPV'
# filePath = r'D:\file2.pdf'
downloadShareableLinkById(fileId, filePath)