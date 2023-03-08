import requests 
from bs4 import BeautifulSoup 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
import datetime 


now = datetime.datetime.now()


# Scraping the Hacker News site 

content = ''

def extract_news(url):
    print('extracting now')
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content 
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cnt += ((str(i+1)+ ' :: ' + tag.text + '\n' + '<br>') if tag.text!='More' else '')
    return cnt 

cnt = extract_news('https://news.ycombinator.com/')
content += cnt 
content += ('<br>'+'-'*50+'<br>')
content += ('<br><br>END OF MESSAGE')

# sending email

SERVER = 'smtp.gmail.com'
PORT = 587 
FROM = 'jmetzg11@gmail.com'
TO = ['jmetzg11@gmail.com', 'jessejmetzger@gmail.com', 'ellinametzger@gmail.com']
PASS = 'tkglrkmjalrtgiyu'

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM 
msg['To'] = ', '.join(TO)

msg.attach(MIMEText(content, 'html'))


print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
