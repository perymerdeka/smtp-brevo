
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = "BREVO API KEY"

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
subject = "Kirim Email dari Production RWID"
html_content = "<html><body><h1>This is my first transactional email </h1></body></html>"
sender = {"name":"Remote Worker Indonesia","email":"noreply.remoteworker.id@gmail.com"}
to = [{"email":"ferilukmansyah@gmail.com","name":"Feril Lukmansyah"}]
cc = [{"email":"hi@hadna.space","name":"Janice Doe"}]
bcc = [{"name":"John Doe","email":"example@example.com"}]
reply_to = {"email":"replyto@domain.com","name":"John Doe"}
headers = {"Some-Custom-Name":"unique-id-1234"}
params = {"parameter":"My param value","subject":"New Subject"}
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, bcc=bcc, cc=cc, reply_to=reply_to, headers=headers, html_content=html_content, sender=sender, subject=subject)

try:
    api_response = api_instance.send_transac_email(send_smtp_email)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)