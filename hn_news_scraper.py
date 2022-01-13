from email.mime.nonmultipart import MIMENonMultipart
import requests #http requests
from bs4 import BeautifulSoup #web scrapping
import smtplib #send the mail
#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime #system date and time manipulataion

now = datetime.datetime.now()

# email content placeholder
content = ''

#extracting Hacker Nwes Stories

def extract_news(url):
  print('Extracting Hacker News Stories...')
  cnt = ''
  cnt +=('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
  response = requests.get(url)
  content = response.content
  soup = BeautifulSoup(content,'html.parser')
  for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
      cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')
  return(cnt)

cnt = extract_news('https://news.ycombinator.com/') #global scope
content+=cnt
content+=('<br>-------------<br>')
content+=('<br><br>End of Message')

#sending email
print('Composing Email')
#update email dtails
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = '' #sender email id
TO='' #receiver email id
PASS='' #password of Sender mail id

msg = MIMEMultipart()
msg['Subject'] = 'Top News Stories HN [Automated Email]' + '' + str(now.day) +'_' + str(now.month) +'_' + str(now.year) 
msg['From'] = FROM
msg['To'] = TO
msg.attach(MIMEText(content, 'html'))

print('Initiating Server')
server = smtplib.SMTP(SERVER, PORT)
#if want to see error message then 1 else 0
server.set_debuglevel(1)
#Extended HELO (EHLO): command sent by an email server to identify itself when connecting to another email server to start the process of sending an email.
server.ehlo()
#StartTLS is a protocol command used to inform the email server that the email client wants to upgrade from an insecure connection to a secure one using TLS or SSL.
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent....')

server.quit()




