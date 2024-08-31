# Automated CSV Download and Email Script

This project consists of a Python script (`autoscript.py`) that automates the process of downloading a CSV file from a website, and then sends the downloaded file via email. The script can be toggled on or off, and it runs only during specified time slots on specified days (New York timezone). The user interface for controlling the script is provided via an HTML file (`button.html`).

## Features

- **Automated Web Interaction**: The script uses Selenium to log in to a website, navigate through it, and download a CSV file.
- **Email Sending**: After downloading the CSV file, it is sent to a specified email address as an attachment.
- **Scheduled Execution**: The script runs only on specified days and within specified time slots (New York timezone).
- **Toggle Control**: A simple toggle switch in the web interface allows the script to be turned on or off.
- **User Interface**: A basic HTML interface allows users to select the day and time slot for the script to run.

## Requirements

- Python 3.x
- `smtplib` (for sending emails)
- `selenium` (for web automation)
- `pytz` (for timezone handling)
- `http.server` (for serving the HTML interface)

## Installation

1. **Install the required Python libraries:**:
   ```bash
   pip install selenium,

   pip install pytz

2. **Download and install the Chrome WebDriver:**

---> Ensure the chromedriver.exe path is correctly specified in the autoscript.py file.

3. **Set up the email credentials:**

  ----> Please ensure to update the receiver and sender email addresses and configure the email app passwords within the `autoscript.py` file.

  ----> Update the send_email_with_attachments function with the correct sender's email and password.


  -----> Place the button.html file in the same directory as `autoscript.py`.


4. **Usage**

   1. Run the Python script:
         
         `python autoscript.py`


    2. Access the web interface:
       
        ----> Open your web browser and go to http://localhost:8080.

        -----> Use the toggle switch to start or stop the script.

        -----> Select the desired day and time slot for the script to run.
    
    3. Schedule Configuration:
        
        -----> The script is pre-configured to run on Tuesdays (1 PM - 2 PM) and Thursdays (3 PM - 4 PM) New York time. 

        -----> You can update these values through the web interface or directly in the script.


5. **File Structure**
      
  ---> autoscript.py: The main Python script that handles automation, scheduling, and email sending.

  ---> button.html: The HTML file for the web interface that allows users to toggle the script and select the day and   time slots.



6. **Customization**
       
 1. Changing the WebDriver Path:
      
    --> Modify the service = Service(r"your_chromedriver_path") line in autoscript.py to point to your Chrome WebDriver execuable.

 2. Download Chrome WebDriver:

   1. -->  Visit the ChromeDriver download page(`https://developer.chrome.com/docs/chromedriver/downloads`).

    ---> On the download page, select the version of ChromeDriver that matches your installed version of Google Chrome. You can check your Chrome version by navigating to chrome://settings/help in your browser.

    ===> Download the appropriate file for your operating system:

        ---->Windows: chromedriver_win32.zip

        --->macOS: chromedriver_mac64.zip

        ---->Linux: chromedriver_linux64.zip

    2. Extract the WebDriver:
       
      ---->After downloading the zip file, extract it to a directory of your choice. This will give you the chromedriver executable file.

    3. Update Your Script:
       
        ----> Modify the service line in your script to point to the location where you extracted the chromedriver. For example, if you extracted it to C:\path\to\chromedriver.exe, your line should look like this:


        ====>  service = `Service(r"C:\path\to\chromedriver.exe")`


        -----> By ensuring that the chromedriver path is correctly specified, your automation script will be able to control the Chrome browser effectively.


