import sendgrid
from sendgrid.helpers.mail import Mail

# Replace this with your actual API Key
SENDGRID_API_KEY = "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"

def send_email(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    email = Mail(
        from_email="siddhartha.chattaraj@associates.scit.edu",
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        response = sg.send(email)
        print(f"✅ Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Example Usage
if __name__ == "__main__":
    to_email = "jaden@rudrasecure.com"  # Change this to the recipient's email
    subject = "Your AI-Powered Newsletter"
    
    # Read the generated newsletter content
    with open("newsletter.md", "r", encoding="utf-8") as file:
        newsletter_content = file.read()

    send_email(to_email, subject, newsletter_content)
