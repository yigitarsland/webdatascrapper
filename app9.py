import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import argparse
from datetime import datetime


# Function to send e-mail using the university mail
def sendEmail(subject, body, config = 'config.json'):
    # Read config file
    config = configparser.ConfigParser()
    config.read(config)

    username = config['username']
    password = config['password']
    smtpServer = config['smtpServer']

    # Create e-mail message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['Subject'] = subject

    # Attach e-mail body
    msg.attach(MIMEText(body, 'plain'))

    # Send e-mail
    try:
        server = smtplib.SMTP(smtpServer)
        server.starttls() # TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted.
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        print('E-mail sent succesfully.')
    except Exception as ex:
        print(f'Failed to send e-mail: {ex}.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send an e-mail to your teacher.')
    parser.add_argument('--mail', type=str, required=True, help='The content of the e-mail')
    args = parser.parse_args()
    emailBody = args.mail
    currentdatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    emailSubject = f'Message sent on {currentdatetime}'
    sendEmail(emailSubject, emailBody)