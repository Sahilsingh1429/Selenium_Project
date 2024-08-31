
# =================================Python Library for Send Email======================================
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime
import pytz

# ================================Selenium Python Library==============================================
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# ==================================HTTP SERVER========================================================

from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
script_running  = False
toggle_on = False 
allowed_days = {
    1: (13, 14),  # Tuesday: 1 PM - 2 PM (13:00 - 14:00)
    2: (10,11),   # Wednesday: 10 AM - 11 AM (10:00 - 11:00)
    3: (15, 16),   # Thursday: 3 PM - 4 PM (15:00 - 16:00)
   
}

# selected_time = None
# selected_day = None

# ===============================REQUEST HANDLER FOR TOGGLE SWITCH=======================================================
class ToggleSwitchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global script_running, toggle_on
        if self.path ==  "/toggle":
            toggle_on = not toggle_on
            script_running = toggle_on and within_schedule()
            status =  "ON" if script_running else "OFF"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(f"Toggled {status}".encode())
            print(f"Script Toggled:{status}")
            if script_running:
                perform_automated_tasks()
            else:
                print("Script turned off")

        elif self.path == '/':
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            with open("button.html","rb") as file:
                self.wfile.write(file.read())

        else:
            self.send_response(404)
            self.end_headers()


    def do_POST(self):
        global allowed_days
        if self.path == "/set_schedule":
            content_length = int(self.headers['Content-Length'])
            post_data =  self.rfile.read(content_length)
            schedule_data =  json.loads(post_data)
            day = int(schedule_data["day"])
            start_houur = int(schedule_data["start_hour"])
            end_hour =  int(schedule_data["end_hour"])
            allowed_days[day] = (start_houur, end_hour)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response =  {"message": "Schedule Updated Sucessully.."}
            self.wfile.write(json.dumps(response).encode())     

def run_server():
    server_address = ('',8080)
    httpd = HTTPServer(server_address,ToggleSwitchHandler)
    httpd.serve_forever()


server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()            
# ========================================NEW_YORK SPECIFIC TIME AND DAYS============================================

def within_schedule():
    global allowed_days
    
    #Get Current time in NewYork timezone..
    ny_tz =  pytz.timezone("America/New_York")
    current_time =  datetime.datetime.now(ny_tz)

    print(f"Current New York Time: {current_time}")

    # Check if today is an allowed day and within the allowed hours..
    if current_time.weekday() in allowed_days :
        start_hour, end_hour  =  allowed_days[current_time.weekday()]
        if start_hour <= current_time.hour < end_hour:
            return True
    return False 

# ================================ALL ACTIONS================================================

def perform_automated_tasks():
    global script_running
    if script_running and within_schedule():
        print("Within Schedule...!! Proceeding with automation and email sending.")
        download_csv()

        # Get the latest downloaded CSV file
        csv_file_path = get_latest_downloaded_file()
        if csv_file_path:
            send_email_with_attachements(csv_file_path)
        else:
            print("No CSV file found in Downloads folder..")

        # Turn off the script after actions are performed
        script_running = False
        print("All actions performed. Script is now turned off.")
    else:
        if not script_running:
            print("Script is currently turned OFF. Toggle it ON to run the script.")
        else:
            print("Current Time is Outside the allowed Schedule.. The Script Will not Run..!!")




def download_csv():
    username = "jimmue@ceofocus.com"
    password = "aBcd123###"


    url = "https://www.freeconferencecallhd.com/login"
    # url = "https://www.freeconferencecallhd.com/profile/account-info-login"


    # Set up Chrome WebDriver
    service = Service(r"D:\DOWNLOAD\chromedriver-win64\chromedriver-win64\chromedriver.exe")

    options = Options()
    options.add_argument("--start-maximized")  # Remove this line if you don't want maximized window

    driver =  webdriver.Chrome(service=service, options=options)

    # Navigate to the login
    driver.get(url)

    # Find username and password fields, and login button
    username_field = driver.find_element(By.ID,"email")
    password_field =  driver.find_element(By.ID,"password")
    login_button =  driver.find_element(By.NAME, "button")


    #Enter the  credentials  and click to the  login button
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

    print("Logged In Sucesfully..!!")

    try:


        #Wait for the "Open Web Controls" button to be clickable and click it
        openweb_controls = WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,"button.btn.btn-primary.btn-lg"))
                )
        sleep(5)
        openweb_controls.click()
        
        print("Clicked on 'open web controls' button Sucessfully..")
        sleep(10)


        #Next Page button to be click...!!  
        nxt_page = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,"button.btn.dropdown-toggle.btn-dropdown.btn-main.dropdown-toggle.btn-default.ember-view"))
                )
        
        sleep(5)
        nxt_page.click()
        sleep(5)

        #Mute Button to be click...!! 
        mute_btn = driver.find_elements(By.CSS_SELECTOR, 'button.btn-mute')
        sleep(2)
        print("Clicked on 'mute button'  Sucessfully..")
        if len(mute_btn) > 1:
            mute_btn[1].click()
        
        sleep(5)
        print("After 'mute button' button..")
        sleep(5)


        #Brodacast Button to be Click..!!
        brodcast = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,"#broadcaster-button"))
        )
        sleep(5)
        print("Brodcast button Sucessfully..")
        brodcast.click()
        print("Click Brodcast button Sucessfully..")
        sleep(5)

        # Broadcast View page to be Shown...!!
        broadcast_view = driver.find_elements(By.CSS_SELECTOR, 'i.fa.fa-volume-up')
        sleep(5)
        print("Clicked on 'broadcast_view button'  Sucessfully..")
        if len(broadcast_view) > 0:
            broadcast_view[0].click()
        sleep(5)
        print("After 'broadcast_view button'..")
        sleep(5)


        # Stop Meeting Buttonto be Click...!!
        stop_meeting = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,"button.stop_meeting.btn.btn-block.btn-red"))
        )   
        sleep(5)
        print("Clicked on the Stop Meeting Button...")
        stop_meeting.click()
        print("Meeting Stop Sucesfully and show the pop-up....")
        sleep(5)


        # Pop-Up Button to be Click...!!
        poppup = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,"button.btn.btn-block.btn-lg.btn-blue"))
        )
        sleep(5)
        print("Clicked on the Yes Button...")
        poppup.click()
        print("Come back to the Previous page Sucessfully...")
        sleep(7)


        # Profile Menu Page View to be Shown...!!
        profile_menu = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,"a.dropdown-toggle.dropdown-toggle.ember-view"))
        )
        sleep(5)
        print("Clicked on the profile_menu Button...")
        profile_menu.click()
        print("Showing All Info of profile_menu Sucessfully...")
        sleep(10)

        #History & Recordings Button to be Click...!!
        history_and_recordings = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ember-view[title='History & Recordings'][href='/profile/history']"))
        )
        sleep(5)
        print("Clicked on the History & Recordings Button...")
        history_and_recordings.click()
        print("Showing All the Details of Rcordings Sucessfully...")
        sleep(10)

        #Info Button to be  Click...!!
        info = WebDriverWait(driver,5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,"button.btn.btn-lg.btn-default"))
        )
        sleep(5)
        print("Clicked on the Info Button...")
        info.click()
        print("Showing All Info and Download-CSV/PDF Options Sucessfully...")
        sleep(10)



        # Download-CSV Button Click and Doownload Start...!!
        download_csv= driver.find_elements(By.CSS_SELECTOR, 'button.btn.btn-lg.btn-light-gray.btn-block')
        sleep(5)
        print("Clicked on the Download-CSV Button...")
        if len(download_csv) > 1:
            download_csv[1].click()
        sleep(10)
        print("Download-CSV File Sucessfully...")
        sleep(20)

    except Exception as e:
        print(f"Error: {str(e)}")



#===============================================================================================================#
                                # For SENDING DOWNLOADED CSV TO EMAIL

def get_latest_downloaded_file():
    download_dir = r"C:\Users\dds07\Downloads"
    files = os.listdir(download_dir)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(download_dir, x)), reverse=True)
    for file in files:
        if file.endswith(".csv"):
            return os.path.join(download_dir,file)
    return None


def send_email_with_attachements(csv_file_path):
    # Email configuration
    sender_email = "singhsahil.dds@gmail.com"
    receiver_email = "sahilr4466@gmail.com"
    subject = "CSV File Downloaded"
    body = "Please Find the CSV File  Attached.."



    # Create a multipart message    
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject


    # Add body to email
    message.attach(MIMEText(body, "plain"))


    # Attach the CSV File 
    with open(csv_file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(csv_file_path)}",
        )
        message.attach(part)

    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, "wbet vtlf rtme saop")
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully..!!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


if __name__ == "__main__":
    print("Server running at http://localhost:8080")
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    while True:
        sleep(2)






# if __name__ == "__main__":
#     if script_running and within_schedule():
#         print("Within Schedule...!! Proceeding with automation and email sending.")
#         download_csv()

#         # Get the latest downloaded CSV file
#         csv_file_path =  get_latest_downloaded_file()
#         if csv_file_path:
#             send_email_with_attachements(csv_file_path)
#         else:
#             print("No CSV file  found in  Downloads folder..")
#     else:
#         if not script_running:
#             print("Script is currently turned OFF. Toggle it ON to run the script..")
#         else:
#             print("Current Time is Outside the allowed Schedule.. The Script Will not Run..!!")
#           # print("The Current New York Time is Outside the Allowed Schedule.. The Script will not Run..!!")

