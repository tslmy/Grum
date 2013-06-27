#
#Informations that you need to edit!!
EMAIL = ''   #Your Google ID(E-mail Address) here.
PASSWORD = ''        #Here goes your password for the mentioned Google ID.
ENTRY_AMOUNT = 20             #(Optional)Amount of the entries you would like me to check.
from urllib import urlencode
from urllib2 import urlopen, Request
import feedparser, html2text #under the same folder
not_for_filename=[u'\\',u'/',u':',u'*',u'?',u'"',u'<',u'>',u'|']
def standardize_file_name(original_filename):
	filename=original_filename
	for character in not_for_filename:
		filename=filename.replace(character,'')
	return filename
#In case of anyone who don't read English.
if EMAIL=='':
	EMAIL=raw_input   ('Email(Google ID):')
if PASSWORD=='':
	PASSWORD=raw_input('Password for it :')
#getting Authorization
request = Request('https://www.google.com/accounts/ClientLogin', urlencode({
    'service': 'reader',
    'Email': EMAIL,
    'Passwd': PASSWORD
}))
print '>Authorizing...'
f = urlopen(request)
lines = f.read().split()
auth = lines[2][5:]
headers = {'Authorization': 'GoogleLogin auth=' + auth}
request = Request('https://www.google.com/reader/atom/user/-/state/com.google/starred-list?n='+str(ENTRY_AMOUNT), headers=headers)
#Use "-" to replace the USER_ID, and Google will replace "-" according to the user that the header described.
f = urlopen(request)
atom = f.read()
d = feedparser.parse(atom)
last_updated_time = d.feed.updated_parsed
print 'Linked to '+d.feed.title+', last updated at '+d.feed.updated+'.'
for entry in d.entries:
    print entry.updated+u'>'+entry.title#+u': '+entry.summary
    try:
        this_summary = entry.summary
    except AttributeError:
        this_summary = ''
    try:
        this_content = entry.content[0]['value']
    except AttributeError:
        this_content = ''
	#from summary and content, select the longer one.
    if len(this_summary)>len(this_content):
        content_HTML=this_summary
    else:
        content_HTML = this_content
    content_Markdown = html2text.html2text(content_HTML)
    f=open(standardize_file_name(entry.title)+'.txt','w+')
    f.write(content_Markdown.replace('\n','\r\n').encode('gb2312','ignore'))#Chinese uses GB code.//Windows uses \r\n.
    f.close()
#print '============ '+str(len(d.entries))+' entries in total =============='
