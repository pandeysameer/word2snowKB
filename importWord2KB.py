import mammoth
import os
from bs4 import BeautifulSoup
from GlideRecord import *

#gr represents the gliderecord for the kb article in servicenow
gr = GlideRecord("kb_template_kcs_article")
gr.set_server("https://dev55004.service-now.com")
gr.set_credentials("admin","pwd")

#next_element will be used later to recursively go through all the elements in the for loop
def next_element(elem):
    while elem is not None:
        #Find next element, skip Navigable String objects
        elem = elem.next_sibling
        if hasattr(elem, 'name'):
            return elem


pages=[]
page=[]

#issue, cause, resolution environment are sections of page.
# In this case, page is a object and issue, resolution, cause etc
# refer to specific elements of the object containing the text.
issue = 0
resolution = 1
cause = 2
environment = 3


path = '.'
filelist = os.listdir(path)
fileCount = 0
sDescription = []
print(filelist)

#Run through all the files in the path
for file in filelist:
    if file.endswith(".docx"):
        fileCount = fileCount + 1
        with open(file, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file)
            html = result.value # The generated HTML
            #soupifyObject = "<html+"</HTML>"
            soup = BeautifulSoup(html,features="html.parser")
            strn = soup.find("h1").text
            sDescription.append(strn.replace("u'","'"))

            print(sDescription)
            #find h2 tags
            h2tags = soup.find_all("h2")

            print(h2tags)
            count = 0
            for h2tag in h2tags:
                page = [str(h2tag)]
                count = count + 1
                elem = next_element(h2tag)
                while elem and elem.name != "h2":
                    page.append(str(elem))
                    elem = next_element(elem)
                pages.append('\n'.join(page))
                #print("Page : ", page)
                #print("Pages: ",pages)

            record_info = {
                "kb_knowledge_base": "IT",
                "short_description": sDescription[fileCount-1],
                "article_type": "text",
                "kb_issue": pages[issue],
                "kb_cause": pages[cause],
                "kb_resolution": pages[resolution],
                "workflow_state": "published",
            }
            #insert this record in ServiceNow
            gr.insert(record_info)
            pages=[]
            page=[]
