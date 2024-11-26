import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import pandas as pd
import os
import time
load_dotenv()  


googleAPIkey = os.getenv("googleAPIkey")
email = os.getenv("email")
phone = os.getenv("phone")
password = os.getenv("password")


with open("Skills_Summary.txt", "r") as f:
    skills_summary = f.read()

# print(f"Skills : {skills_summary}")

def generate_personalised_paragraph(company_name):
    prompt = f"""Research the company {company_name} and, based on publicly available information or general assumptions, write a short personalized paragraph about how my skills align with {company_name}. Use the following skills: {skills_summary}. 
If you cannot find specific details about the company, assume it is a forward-thinking tech company working on innovative projects in software development, AI/ML, and cloud technologies. Write the paragraph accordingly. 
Focus on aligning the most relevant skills from the list with typical goals or values of a tech company, such as innovation, scalability, or efficiency.
"""

    llm = GoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=googleAPIkey)
    response = llm.invoke(prompt)
    print("response created!")
    return response



def send_email(sender_email,sender_name,recipient_email,subject,html_body,resume_path):
    print("starting to send email")
    message=MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(html_body, "html"))

    with open(resume_path,'rb') as f:
        resume=MIMEText(f.read(),'base64','utf-8')
        resume.add_header("Content-Disposition", "attachment", filename="Resume.pdf")
        message.attach(resume)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email,password)
        server.sendmail(sender_email, recipient_email, message.as_string())
    print("email sent!")


def automate_emails(csv_path,sender_email, sender_name, resume_path):
    data = pd.read_csv(csv_path)

    for index, row in data.iterrows():
        founder_name = row["Founder Name"]
        company_name = row["Company Name"]
        recipient_email = row["Founder Email"]

        personalised_para_abt_company = generate_personalised_paragraph(company_name)

        template = f"""
        <html>
            <body>
                <p>Hi <b>{founder_name}</b>,</p>

                <p>I hope you're doing well. I am writing to express my interest in the <b>SDE Intern</b> position at <b>{company_name}</b> for next 6 months. I have attached my updated resume for your review.</p>

                <p><b>Experience:</b></p>
                <ul>
                    <li><b>Backend Intern at Avinyaz:</b> Designed a complete microservice, improved existing services, and built key modules like audio generation and LangChain integration for OpenAI models. I also reduced API costs by 30% through monitoring and optimization.</li>
                    <li><b>Technical Head at Oculus S.P.I.T.:</b> I also led development of a real-time IPL auction app for a college event with over <b>20 live auctions & 252 participating players</b>, managed databases, and created efficient APIs to ensure smooth operation.</li>
                </ul>

                <p><b>Achievements:</b></p>
                <ul>
                    <li>Placed in the top 15 in <b>Barclays’ National Hackathon</b>, selected from over <b>4,000 teams</b> across India.</li>
                    <li>Secured <b>3140th globally</b> out of 19,630 participants in LeetCode Biweekly Contest 130.</li>
                    <li>Achieved a peak rating of <b>1714</b> on LeetCode, placing in the top <b>12%</b> of users globally.</li>
                </ul>

                <p>{personalised_para_abt_company}</p>

                <p><b>Personal Details:</b><br>
                Email: <b>{email}</b><br>
                Phone: <b>{phone}</b></p>

                <p>I believe my technical skills and problem-solving abilities make me a strong fit for the <b>SDE Intern</b> role at <b>{company_name}</b>. I would love the opportunity to contribute to your team and help drive <b>{company_name}</b>'s success.</p>

                <p>Looking forward to hearing from you!</p>

                <p>Best regards,<br>
                <b>{sender_name}</b></p>
            </body>
        </html>
        """
        print("Template created!")
        send_email(sender_email, sender_name, recipient_email,f"Application for SDE Intern Position at {company_name}",template,resume_path)
        if index != len(data) - 1:  
            print("Waiting for 4 minutes before sending the next email...")
            time.sleep(240)  
    
    print("All emails sent successfully!")

# csv_path = "data.csv"
# resume_path = "/path/to/resume.pdf"
# sender_email = "your_email@gmail.com"
# sender_name = "Your Name"

csv_path = "data.csv"
resume_path = "../../MY RESUME_DEVANG/resume4/Devang_Vartak_resume.pdf"
sender_email = ""
sender_name = "Devang Vartak"

try:
    automate_emails(csv_path,sender_email, sender_name, resume_path)
    print("Emails sent successfully 🥳🥂!")
except Exception as e:
    print(e)



