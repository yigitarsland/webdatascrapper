import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import argparse
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# Function to send e-mail using the university mail
def sendEmail(emailSubject, body, config = 'config.json'):
    # Read config file
    with open(config, 'r') as file:
        config = json.load(file)

    username = config['username']
    password = config['password']
    smtpServer = config['smtpServer']

    # Create e-mail message
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = 'yigitarsland@icloud.com' 
    msg['Subject'] = 'Yigit Arslan ' + emailSubject

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

def getCatFacts(amount):
    url = 'https://cat-fact.herokuapp.com/facts/random'
    params = {
        "animal_type": "cat",
        "amount": amount
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json() # Parse json response directly
        for fact in data:
            print(fact['text'])
    else:
            print("Please specify the number of cat facts to retrieve.")
            
# Function to report list of researchers of W4N PWr department with last names starting with a given letter.
def fetchResearchers(letter):
    url = f'https://wit.pwr.edu.pl/wydzial/struktura-organizacyjna/pracownicy?letter={letter}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data for letter {letter}.")
        return 
    
    soup = BeautifulSoup(response.text, 'html.parser')
    researchers = []

    researcher_entries = soup.find_all('div', class_='col-text text-content') 
    for entry in researcher_entries:
        name = entry.find('a').text.strip()
        email_tag = entry.find('p')
        email = email_tag.text.strip() if email_tag else 'No email available'
        researchers.append(f"{name} - {email}")
        
    if not researchers:
        print(f"No researchers found with the last name starting with '{letter}'.")
    else:
        print(f"The list of researchers - {letter}")
        for researcher in researchers:
            print(researcher)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send an e-mail to your teacher or get random cat facts.')
    parser.add_argument('--mail', type=str, help='The content of the e-mail')
    parser.add_argument("--catfacts", type= int, help="Number of cat facts to retrieve")
    parser.add_argument('--fetchresearchers', type=str, help="Letter of the targeted surname")
    args = parser.parse_args()

    if args.mail:
        emailBody = args.mail
        currentdatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        emailSubject = f'Message sent on {currentdatetime}'
        sendEmail(emailSubject, emailBody)
    elif args.catfacts:
        getCatFacts(args.catfacts)
    elif args.fetchresearchers:
        fetchResearchers(args.fetchresearchers)
