import smtplib

smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.ehlo()
smtp_server.starttls()
smtp_server.login('disc.assessment.results@gmail.com', 'ngpb dgna afkw guuu')

smtp_server.sendmail('disc.assessment.results@gmail.com', 'ethan.a.smith@hotmail.co.uk', 'Subject: Happy Australia Day!nHi Everyone! Happy Australia Day! Cheers, Julian')

smtp_server.quit()
print('Email sent successfully')