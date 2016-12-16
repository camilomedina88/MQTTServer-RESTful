import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
 
fromaddr = "monitorredpanda@gmail.com"
toaddr = "nicolas.velasquez531@gmail.com"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "REDPANDA ALERT"
 
body = "Hola Nico.. Dejemos asiiii.... Informe y saleee"
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "camilomedina")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()