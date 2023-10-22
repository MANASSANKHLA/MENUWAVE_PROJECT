from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import mysql.connector
import requests
import base64



global menu
menu=[]
# global bb
# global ab
bb=""
ab=""
global T
global email
global F
signin=False
F=False
T=True



db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': '',
    'port': 
}

connection = mysql.connector.connect(**db_config)




app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#-------------------------------------
#-------------------------------------
#-------------------------------------
#START OF INDEX PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------


@app.route('/contact', methods=['POST'])
def contact():
    temp_name = request.form['t_name']
    temp_email = request.form['t_email']
    temp_des = request.form['t_des']
    print(temp_name, temp_email, temp_des)
             # Email configuration
    smtp_server = ''  # Replace with your SMTP server address
    smtp_port =   # Replace with the appropriate port for your SMTP server
    sender_email = ''  # Replace with your email address
    sender_password = ''  # Replace with your email password
    recipient_email = ''  # Replace with the recipient's email address

    # Email content
    subject = 'Feedback From a User'
    message = f'Name of the user: {temp_name}\nEmail of User: {temp_email}\nMessage from User: {temp_des}'

    # Create a multipart message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

        # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

        # Create a secure connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

        # Send the email
    server.send_message(msg)

        # Close the SMTP connection
    server.quit()
    return render_template('index.html', output="Feedback Send Successfully") 
#-------------------------------------
#-------------------------------------
#-------------------------------------
#END OF INDEX PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


#-------------------------------------
#-------------------------------------
#-------------------------------------
#START OF SIGN UP PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------


# Sending OTP to Mail


@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        global g_email, g_name, g_pass, ver
        email = request.form['email']
        name = request.form['u_name']
        password = request.form['pass']
        g_email=email
        g_name= name
        g_pass=password
        random_number = random.randint(1000, 9999)
        ver=random_number


        #Verifying Email Duplication

        mail_dup()
        if ab==1:
            return render_template('sign_up.html', show_element1=T, show_element2=F, output="User Already Exist")
        elif ab==0:

            # Email configuration
            smtp_server = ''  # Replace with your SMTP server address
            smtp_port =  # Replace with the appropriate port for your SMTP server
            sender_email = ''  # Replace with your email address
            sender_password = ''  # Replace with your email password
            recipient_email = email  # Replace with the recipient's email address

            # Email content
            subject = 'OTP from MenuWave'
            message = f'OTP: {ver}'

            # Create a multipart message object
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Attach the message to the email
            msg.attach(MIMEText(message, 'plain'))

            # Create a secure connection to the SMTP server
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)

            # Send the email
            server.send_message(msg)

            # Close the SMTP connection
            server.quit()
                    
            return render_template('sign_up.html', show_element1=F, show_element2=T, output2="Check your Email")
        return render_template('sign_up.html', show_element1=T, show_element2=F, output="Something Went Wrong")
    except Exception as e:
        return f'Failed to send email. Error: {str(e)}'


#Mail Duplications Check

def mail_dup():
     cursor = connection.cursor()
     cursor.execute(f"select email from users;")
     result = cursor.fetchall()
     global ab
     ab=0
     for row in result:
        v = str(row)
        value=v.strip("(),'")
        if g_email==value:
            ab=1
        else:
            pass


# Verify Mail 


@app.route('/mail_verify', methods=['POST'])
def mail_verify():
    veri=request.form['ver']
    verify=int(veri)
    if verify==ver:
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO users (u_name, email, u_pass) VALUES ('{g_name}', '{g_email}', '{g_pass}');")
        connection.commit()
        return render_template('sign_in.html', output="Your account is Created")
    elif verify!=ver:
        output2="You are not Verified"
        return render_template('sign_up.html', output2=output2, show_element1=F, show_element2=T)
    return render_template('sign_up.html', output="Something went wrong")




#-------------------------------------
#-------------------------------------
#-------------------------------------
#END OF SIGN UP PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


#-------------------------------------
#-------------------------------------
#-------------------------------------
#START OF SIGN IN PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------



@app.route('/sign_in_email_verification', methods=['GET','POST'])
def sign_in_email_verification():
    global signin
    if request.method=='POST':
        global email
        email = request.form['email']
        u_pass = request.form['pass']
        cursor = connection.cursor()
        cursor.execute(f"select email from users where email='{email}';")
        result = cursor.fetchall()
        check_email=f"[('{email}',)]"
        if str(result)==check_email:
            cursor.execute(f"select email, u_pass from users where email='{email}';")
            result = cursor.fetchall()
            credentials=f"[('{email}', '{u_pass}')]"
            if str(result)==credentials:
                signin=True
                cursor.execute(f'SELECT email FROM users WHERE email="{email}" AND link is NOT NULL;')
                c1 = cursor.fetchall()
                e1=f"[('{email}',)]"
                r1=str(c1)
                if e1==r1:
                    return render_template('home.html', show_element2=True, moutput="Menu Card Already Exist")
                elif e1!=r1:
                    return render_template('home.html', show_element1=True)
                else:
                    return render_template('sign_in.html', output="Something went wrong")
            elif str(result)!=credentials:
                return render_template('sign_in.html', output="Wrong Credentials")
            else:
                return render_template('sign_in.html', output="Something Went Wrong")
        elif str(result)!=check_email:
            return render_template('sign_in.html', output="Your email doesn't exist")
        else:
            return render_template('sign_in.html', output="Something Went Wrong")
    else:
        return render_template('sign_in.html', output="ERROR")

#-------------------------------------
#-------------------------------------
#-------------------------------------
#END OF SIGN IN PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


#-------------------------------------
#-------------------------------------
#-------------------------------------
#START OF FORGET PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------

@app.route('/forget', methods=['POST'])
def forget():
    email = request.form['email']
    cursor = connection.cursor()
    cursor.execute(f"select email from users where email='{email}';")
    result = cursor.fetchall()
    check_email=f"[('{email}',)]"
    if str(result)==check_email:
        cursor.execute(f"select u_pass from users where email='{email}';")
        r1 = cursor.fetchall()
         # Email configuration
        smtp_server = ''  # Replace with your SMTP server address
        smtp_port =  # Replace with the appropriate port for your SMTP server
        sender_email = ''  # Replace with your email address
        sender_password = ''  # Replace with your email password
        recipient_email = email  # Replace with the recipient's email address

        # Email content
        subject = 'Password of your email from MenuWave'
        message = f'Password: {r1}'

        # Create a multipart message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message to the email
        msg.attach(MIMEText(message, 'plain'))

        # Create a secure connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.send_message(msg)

        # Close the SMTP connection
        server.quit()
        return render_template('forget.html', output='Please check your Mail')
    elif str(result)==check_email:
        return render_template('forget.html', output="This Mail Doesn't Exist")
    else:
        return render_template('forget.html', output="Something went Wrong")


#-------------------------------------
#-------------------------------------
#-------------------------------------
#END OF FORGET PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


#-------------------------------------
#-------------------------------------
#-------------------------------------
#START OF HOME PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------

@app.route('/delete')
def delete():
    menu.clear()
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET resto_name = NULL, link = NULL WHERE email = "{email}";')
    connection.commit()
    def delete_file(access_token, owner, repo, file_path, branch):
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'

        # Set the headers with the access token
        headers = {
        'Authorization': f'Token {access_token}',
        'Accept': 'application/vnd.github.v3+json'
        }

        # Get the file details
        response = requests.get(url, headers=headers)
        file_data = response.json()
    
        if 'sha' not in file_data:
            print('Failed to retrieve file information.')
            print(file_data)
            return

        # Extract the SHA hash of the file
        file_sha = file_data['sha']

        # Set the deletion parameters
        deletion_params = {
            'message': 'Delete file',
            'sha': file_sha,
            'branch': branch
            }

        # Send the DELETE request to delete the file
        response = requests.delete(url, headers=headers, json=deletion_params)

        # Check the response status
        if response.status_code == 200:
            print('File deleted successfully.')
            
        else:
            print('Failed to delete the file.')
            print(response.json())
        # Provide your access token, repository information, file path, and branch
    access_token = ''
    owner = ''
    repo = ''
    branch = ''

    # Call the delete_file function
    file_path = f'{email}/menuwave.html'
    delete_file(access_token, owner, repo, file_path, branch)
    file_path = f'{email}/qr_code.png'
    delete_file(access_token, owner, repo, file_path, branch)
    return render_template('home.html', output="File Deleted Successfully", show_element1=True)
    

@app.route('/show_qr')
def show_qr():
    return render_template('qr.html', email=email)

#-------------------------------------
#-------------------------------------
#-------------------------------------
#END OF HOME PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


#-------------------------------------
#-------------------------------------
#-------------------------------------
#START OF DETAILS PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------

#Name of the Restaurant
@app.route('/restro_name', methods=['POST'])
def restro_name():
    global res_name
    res_name = request.form['therestro']
    cursor = connection.cursor()
    cursor.execute(f'UPDATE users SET resto_name = "{res_name}" WHERE email = "{email}"')
    connection.commit()
    return render_template('details.html', show_element3=T)



#Name of Category
@app.route('/cat_name', methods=['POST'])
def cat_name():
    global category, c_name
    global ab
    c_name = request.form['name_category']
    category = [c_name]
    menu.append(category)
    print(menu)

    return render_template('details.html', show_element5=T)

#, output2=bb
#Dish Name, Price, Desciption
@app.route('/n_dish_prc_des', methods=['POST'])
def n_dish_prc_des():
    global bb
    d_name = request.form['dish_name']
    d_prc = request.form['dish_prc']
    d_desc = request.form['dish_des']
    action = request.form['action']
    for c_index, m in enumerate(menu):
        index=0
        print(c_index, menu)
        print(f"m: {m}")
        print(f"c: {category}")
    if m==category:
        index=c_index
        print(index, type(index))
    else:
        return category, m, "Something Went Wrong"
    full=[d_name, d_prc, d_desc] 
    menu[index].append(full)
    if action == 'action1':
        print(menu)
        return render_template('choose_menu.html')
    elif action == 'action2':
        # bb+=f"{d_name}, {d_prc}, {d_desc}"
        # cd+=bb
        return render_template('details.html', show_element5=T)
        # for n, m in enumerate(menu):
        #     print(m)
        #     for b, a in enumerate(m):
        #         print(a)
        #         bb+=f"{d_name}, {d_prc}, {d_desc}"
        
    elif action == 'action3':
        # bb+=f"{d_name}, {d_prc}, {d_desc}"
        # cd+=bb
        # for n, m in enumerate(menu):
        #     print(m)
        #     for b, a in enumerate(m):
        #         print(a)
        #         bb+=f"{d_name}, {d_prc}, {d_desc}"
        return render_template('details.html', show_element3=T)
 
@app.route('/new_dish')
def new_dish():
    return render_template('details.html', show_element5=T)



#-------------------------------------
#-------------------------------------
#-------------------------------------
#END OF DETAILS PAGE
#-------------------------------------
#-------------------------------------
#-------------------------------------


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


#-------------------------------------
#-------------------------------------
#-------------------------------------
#START OF CHOOSING MENU
#-------------------------------------
#-------------------------------------
#-------------------------------------

#---------------------------------
#FIRST MENU CARD
#---------------------------------

@app.route('/menu_card2')
def menu_card2():
    #------------------------
    #MENU FILE GENERATION
    #------------------------
    repository=""
    file_path=f"{email}/"
    branch = ""
    access_token = ""
    url = f""
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    start_box = """
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap" rel="stylesheet">

  <title>Restaurant Menu</title>
  <style>
/* Reset some default styles */
body, h1, h2, h3, p, ul, li {
    margin: 0;
    padding: 0;
  }

 body
  {
    background-color: #3B3B3B;
    ;
  }
  
  body {
    font-family: 'Roboto Mono', monospace;
  }

  .last_line
  {
    margin-top: 10px;
    text-align: center;
  }
  
  /* Header Styles */
  header {
    background: #FFFFFF;
    border: 1px solid #000000;
    box-shadow: 10px 10px 0px #000000;
    margin: 20px;
    padding: 20px;
    text-align: center;
  }
  
  .title {
    font-size: 24px;
  }
  
  /* Menu Styles */
  .menu {
    margin-left: 20px;
    height: 750px;
    margin-right: 20px;
    padding: 20px;
    overflow: auto;
    background: #FFFFFF;
    border: 1px solid #000000;
    box-shadow: 10px 10px 0px #000000;
  }
  
  .category {
    margin-top: 10px;
    margin-bottom: 30px;
  }
  
  .category-name {
    text-transform: uppercase;
    color: #ffffff;
    text-align: center;
    padding: 10px;
    font-size: 20px;
    margin-bottom: 10px;
    background: #3B3B3B;
    border: 1px solid #000000;
    box-shadow: 5px 5px 0px #000000;
  }
  
  .dishes {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }

  .dish {
    background: #FFFFFF;
    border: 1px solid #000000;
    box-shadow: 5px 5px 0px #000000;
    padding: 20px;
  }
  
  .dish-name {
    color: #000000;
    font-size: 18px;
    margin-bottom: 10px;
  }
  
  .dish-price {
    color: #000000;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .dish-description {
    color: #353535;
    font-size: 14px;
    margin-top: 10px;
  }
  
  /* Responsive Styles */
  @media screen and (max-width: 768px) {
    .menu {
      padding: 10px;
    }
    
    .dishes {
      grid-template-columns: 1fr;
    }
    
    .dish {
      margin-bottom: 20px;
    }
  }

  /* Menu_Card_Resizing */

  @media screen and (max-height: 1000px){
    .menu{
        height: 800px;
    }
    
  }

  @media screen and (max-height: 950px){
    .menu{
        height: 750px;
    }
    
  }

  @media screen and (max-height: 900px){
    .menu{
        height: 700px;
    }
    
  }

  
  @media screen and (max-height: 850px){
    .menu{
        height: 650px;
    }
    
  }

  @media screen and (max-height: 800px){
    .menu{
        height: 600px;
    }
    
  }

  @media screen and (max-height: 750px){
    .menu{
        height: 550px;
    }
    
  }

  @media screen and (max-height: 700px){
    .menu{
        height: 500px;
    }
    
  }
  
  @media screen and (max-height: 650px){
    .menu{
        height: 450px;
    }
    
  }

  @media screen and (max-height: 600px){
    .menu{
        height: 400px;
    }
    
  }

  </style>
</head>
    <body>
        <div class="bg">
            <header>
                <h1 class="title">"""+res_name+"""</h1>
            </header>
            <div class="menu">
    """

    end_box = """
            </div>
        </div>
    </body>
    </html>
    """

    file_content = start_box

    for item in menu:
        category = item[0]
        dishes = item[1:]

        file_content += f'<div class="category">'
        file_content += f'<h2 class="category-name">{category}</h2>'

        for dish in dishes:
            dish_name = dish[0]
            dish_price = dish[1]
            dish_description = dish[2]

            file_content += '<div class="dishes">'
            file_content += '<div class="dish">'
            file_content += f'<h3 class="dish-name">{dish_name}</h3>'
            file_content += f'<p class="dish-price">{dish_price}/-</p>'
            file_content += f'<p class="dish-description">{dish_description}</p>'
            file_content += '</div>'
            file_content += '</div>'

        file_content += '</div>'

    file_content += end_box

    print(file_content)

    encoded_content = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")

    data = {
        "message": "Create HTML file",
        "content": encoded_content,
        "branch": branch
    }
    response = requests.put(url, headers=headers, json=data)
    print(response)
    if response.status_code == 201:
        print("File created successfully.")
    else:
        print("File creation failed.")

    #------------------------
    #QR_CODE GENERATION
    #------------------------
    
    qr_data=f'''https://api.qrserver.com/v1/create-qr-code/?data=https%3A%2F%2Flabdhpurohit.github.io/Menu_Wave_Files/{email}/menuwave.html&size=300'''

    #------------------------
    #STORING LINK IN QR CODE
    #------------------------

    cursor = connection.cursor()
    cursor.execute(f"UPDATE users SET link = '{qr_data}' WHERE email = '{email}'")
    connection.commit()
    
    #------------------------
    #SENDING QR_CODE AND URL TO CONSUMER's EMAIL
    #------------------------

    sender_email = ""
    receiver_email = email
    password = ""
    message = MIMEMultipart("related")
    message["Subject"] = "Menu Card with QR Code"
    message["From"] = sender_email
    message["To"] = receiver_email


    # Email content
    email_content = f"""
    <html>
    <body>
        <h2>Menu Card</h2>
        <p>Dear Customer,</p>
        <p>Thank you for choosing MenuWave. Here is our menu card with a QR code:</p>
        <img src="{qr_data}">
        <p>You can scan the QR code or click the link below to access our menu online:</p>
        <a href="">Menu Card</a>
        <p>Enjoy your meal!</p>
    </body>
    </html>
    """
    # Attach email content as HTML
    email_body = MIMEText(email_content, "html")
    message.attach(email_body)


    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", str(e))

    return render_template('home.html', show_element2=True, moutput="Menu Card Created Successfully")    
#---------------------------------
#SECOND MENU CARD
#---------------------------------

@app.route('/menu_card1')
def menu_card1():
    #------------------------
    #MENU FILE GENERATION
    #------------------------
    repository="labdhpurohit/Menu_Wave_Files"
    file_path=f"{email}/menuwave.html"
    branch = "main"
    access_token = ""
    url = f"https://api.github.com/repos/{repository}/contents/{file_path}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    start_box = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Overpass:wght@300&display=swap" rel="stylesheet">
        <title>Restaurant Menu</title>
        <style>
            /* Reset some default styles */
            body, h1, h2, h3, p, ul, li {
                margin: 0;
                padding: 0;
            }

            body {
                background-image: url('https://labdhpurohit.github.io/Menu_Example1/bg_f.png');
                background-size: 250%;
                background-position: center;
                background-color: #000000;
                font-family: 'Overpass', sans-serif;
            }

            .last_line {
                text-align: center;
                color: #ffd498;
            }

            /* Header Styles */
            header {
                background: rgba(19, 19, 19, 0.5);
                box-shadow: 10px 10px 50px #000000;
                backdrop-filter: blur(25px);
                -webkit-backdrop-filter: blur(25px);
                border-radius: 12px;
                margin: 20px;
                padding: 20px;
                color: #FFC370;
                text-align: center;
            }

            .title {
                font-size: 24px;
            }

            /* Menu Styles */
            .menu {
                margin-left: 20px;
                height: 750px;
                margin-right: 20px;
                padding: 20px;
                background: rgba(19, 19, 19, 0.5);
                box-shadow: 10px 10px 50px #000000;
                border-radius: 12px;
                overflow: auto;
                -webkit-backdrop-filter: blur(25px);
                backdrop-filter: blur(25px);
                border-radius: 12px;
            }

            .category {
                margin-top: 10px;
                margin-bottom: 30px;
            }

            .category-name {
                color: #FFC370;
                font-size: 20px;
                margin-bottom: 10px;
            }

            .dishes {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }

            .dish {
                background: rgba(16, 16, 16, 0.5);
                box-shadow: inset 0px 0px 50px rgba(0, 0, 0, 0.5);
                padding: 20px;
                border-radius: 12px;
            }

            .dish-name {
                color: #FFB140;
                font-size: 18px;
                margin-bottom: 10px;
            }

            .dish-price {
                color: #FFB140;
                font-weight: bold;
                margin-bottom: 5px;
            }

            .dish-description {
                color: #ffbf64;
                font-size: 14px;
                margin-top: 10px;
            }

            /* Responsive Styles */
            @media screen and (max-width: 768px) {
                .menu {
                    padding: 10px;
                }

                .dishes {
                    grid-template-columns: 1fr;
                }

                .dish {
                    margin-bottom: 20px;
                }
            }

            /* Menu_Card_Resizing */
            @media screen and (max-height: 1000px) {
                .menu {
                    height: 800px;
                }
                body {
                    background-size: 100%;
                }
            }

            @media screen and (max-height: 950px) {
                .menu {
                    height: 750px;
                }
                body {
                    background-size: 150%;
                }
            }

            @media screen and (max-height: 900px) {
                .menu {
                    height: 700px;
                }
                body {
                    background-size: 200%;
                }
            }

            @media screen and (max-height: 850px) {
                .menu {
                    height: 650px;
                }
                body {
                    background-size: 250%;
                }
            }

            @media screen and (max-height: 800px) {
                .menu {
                    height: 600px;
                }
                body {
                    background-size: 300%;
                }
            }

            @media screen and (max-height: 750px) {
                .menu {
                    height: 550px;
                }
                body {
                    background-size: 350%;
                }
            }

            @media screen and (max-height: 700px) {
                .menu {
                    height: 500px;
                }
                body {
                    background-size: 350%;
                }
            }

            @media screen and (max-height: 650px) {
                .menu {
                    height: 450px;
                }
                body {
                    background-size: 350%;
                }
            }

            @media screen and (max-height: 600px) {
                .menu {
                    height: 400px;
                }
                body {
                    background-size: 350%;
                }
            }
        </style>
    </head>
    <body>
        <div class="bg">
            <header>
                <h1 class="title">"""+res_name+"""</h1>
            </header>
            <div class="menu">
    """

    end_box = """
            </div>
        </div>
    </body>
    </html>
    """

    file_content = start_box

    for item in menu:
        category = item[0]
        dishes = item[1:]

        file_content += f'<div class="category">'
        file_content += f'<h2 class="category-name">{category}</h2>'

        for dish in dishes:
            dish_name = dish[0]
            dish_price = dish[1]
            dish_description = dish[2]

            file_content += '<div class="dishes">'
            file_content += '<div class="dish">'
            file_content += f'<h3 class="dish-name">{dish_name}</h3>'
            file_content += f'<p class="dish-price">{dish_price}/-</p>'
            file_content += f'<p class="dish-description">{dish_description}</p>'
            file_content += '</div>'
            file_content += '</div>'

        file_content += '</div>'

    file_content += end_box

    print(file_content)

    encoded_content = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")

    data = {
        "message": "Create HTML file",
        "content": encoded_content,
        "branch": branch
    }
    response = requests.put(url, headers=headers, json=data)
    print(response)
    if response.status_code == 201:
        print("File created successfully.")
    else:
        print("File creation failed.")

    #------------------------
    #QR_CODE GENERATION
    #------------------------
    
    qr_data=f'''https://api.qrserver.com/v1/create-qr-code/?data=https%3A%2F%2Flabdhpurohit.github.io/Menu_Wave_Files/{email}/menuwave.html&size=300'''

    #------------------------
    #STORING LINK IN QR CODE
    #------------------------

    cursor = connection.cursor()
    cursor.execute(f"UPDATE users SET link = '{qr_data}' WHERE email = '{email}'")
    connection.commit()
    
    #------------------------
    #SENDING QR_CODE AND URL TO CONSUMER's EMAIL
    #------------------------

    sender_email = ""
    receiver_email = email
    password = ""
    message = MIMEMultipart("related")
    message["Subject"] = "Menu Card with QR Code"
    message["From"] = sender_email
    message["To"] = receiver_email


    # Email content
    email_content = f"""
    <html>
    <body>
        <h2>Menu Card</h2>
        <p>Dear Customer,</p>
        <p>Thank you for choosing MenuWave. Here is our menu card with a QR code:</p>
        <img src="{qr_data}">
        <p>You can scan the QR code or click the link below to access our menu online:</p>
        <a href="https://labdhpurohit.github.io/Menu_Wave_Files/{email}/menuwave.html">Menu Card</a>
        <p>Enjoy your meal!</p>
    </body>
    </html>
    """
    # Attach email content as HTML
    email_body = MIMEText(email_content, "html")
    message.attach(email_body)


    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", str(e))

    return render_template('home.html', show_element2=True, moutput="Menu Card Created Successfully")    
#---------------------------------
#THIRD MENU CARD
#---------------------------------

@app.route('/menu_card3')
def menu_card3():
    #------------------------
    #MENU FILE GENERATION
    #------------------------
    repository=""
    file_path=f"{email}/"
    branch = "main"
    access_token = ""
    url = f"https://api.github.com/repos/{repository}/contents/{file_path}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    start_box = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Overpass:wght@300&display=swap" rel="stylesheet">
        <title>Restaurant Menu</title>
            <style>
/* Reset some default styles */
body, h1, h2, h3, p, ul, li {
    margin: 0;
    padding: 0;
  }

 body
  {
    background-image: url('https://labdhpurohit.github.io/Menu_Example3/Untitled%20design%20(1).gif');
    background-size: cover;
    background-position: center;
    background-color: #ffe76e;
  }
  
  body {
    font-family: 'Overpass', sans-serif;
  }

  .last_line
  {
    text-align: center;
    color: #ffd498;
  }
  
  /* Header Styles */
  header {
    border-radius: 10px;
    border: 1px solid #000;
    background: rgba(255, 255, 255, 0.20);
    box-shadow: 10px 10px 0px 0px #613400;
    backdrop-filter: blur(2.5px);
    -webkit-backdrop-filter: blur(2.5px);
    margin: 20px;
    padding: 20px;
    color: #291600;
    text-align: center;
  }
  
  .title {
    font-size: 24px;
  }
  
  /* Menu Styles */
  .menu {
    margin-left: 20px;
    height: 750px;
    margin-right: 20px;
    padding: 20px;
    overflow: auto;
    border-radius: 10px;
border: 1px solid #000;
background: rgba(255, 255, 255, 0.20);
box-shadow: 10px 10px 0px 0px #613400;
backdrop-filter: blur(2.5px);
    -webkit-backdrop-filter: blur(2.5px);
  }
  
  .category {
    margin-top: 10px;
    margin-bottom: 30px;
  }
  
  .category-name {
    color: #291600;
    font-size: 20px;
    margin-bottom: 10px;
  }
  
  .dishes {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .dish {
    border-radius: 10px;
border: 1px solid #000;
background: rgba(255, 255, 255, 0.20);
box-shadow: 5px 5px 0px 0px #613400;
backdrop-filter: blur(2.5px);
    padding: 20px;
    
  }
  
  .dish-name {
    color: #291600;
    font-size: 18px;
    margin-bottom: 10px;
  }
  
  .dish-price {
    color: #291600;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .dish-description {
    color: #291600;
    font-size: 14px;
    margin-top: 10px;
  }
  
  /* Responsive Styles */
  @media screen and (max-width: 768px) {
    .menu {
      padding: 10px;
    }
    
    .dishes {
      grid-template-columns: 1fr;
    }
    
    .dish {
      margin-bottom: 20px;
    }
  }

  /* Menu_Card_Resizing */

  @media screen and (max-height: 1000px){
    .menu{
        height: 800px;
    }
    body{
        background-size: 100%;
    }
    
  }

  @media screen and (max-height: 950px){
    .menu{
        height: 750px;
    }
    body{
        background-size: 150%;
    }
    
  }

  @media screen and (max-height: 900px){
    .menu{
        height: 700px;
    }
    body{
        background-size: 200%;
    }
    
  }

  
  @media screen and (max-height: 850px){
    .menu{
        height: 650px;
    }
    body{
        background-size: 250%;
    }
    
  }

  @media screen and (max-height: 800px){
    .menu{
        height: 600px;
    }
    body{
        background-size: 300%;
    }
    
  }

  @media screen and (max-height: 750px){
    .menu{
        height: 550px;
    }
    body{
        background-size: 350%;
    }
    
  }

  @media screen and (max-height: 700px){
    .menu{
        height: 500px;
    }
    body{
        background-size: 350%;
    }
    
  }
  
  @media screen and (max-height: 650px){
    .menu{
        height: 450px;
    }
    body{
        background-size: 350%;
    }
    
  }

  @media screen and (max-height: 600px){
    .menu{
        height: 400px;
    }
    body{
        background-size: 350%;
    }
    
  }

    </style>
    </head>
    <body>
        <div class="bg">
            <header>
                <h1 class="title">"""+res_name+"""</h1>
            </header>
            <div class="menu">
    """

    end_box = """
            </div>
        </div>
    </body>
    </html>
    """

    file_content = start_box

    for item in menu:
        category = item[0]
        dishes = item[1:]

        file_content += f'<div class="category">'
        file_content += f'<h2 class="category-name">{category}</h2>'

        for dish in dishes:
            dish_name = dish[0]
            dish_price = dish[1]
            dish_description = dish[2]

            file_content += '<div class="dishes">'
            file_content += '<div class="dish">'
            file_content += f'<h3 class="dish-name">{dish_name}</h3>'
            file_content += f'<p class="dish-price">{dish_price}/-</p>'
            file_content += f'<p class="dish-description">{dish_description}</p>'
            file_content += '</div>'
            file_content += '</div>'

        file_content += '</div>'

    file_content += end_box

    print(file_content)

    encoded_content = base64.b64encode(file_content.encode("utf-8")).decode("utf-8")

    data = {
        "message": "Create HTML file",
        "content": encoded_content,
        "branch": branch
    }
    response = requests.put(url, headers=headers, json=data)
    print(response)
    if response.status_code == 201:
        print("File created successfully.")
    else:
        print("File creation failed.")

    #------------------------
    #QR_CODE GENERATION
    #------------------------
    
    qr_data=f'''https://api.qrserver.com/v1/create-qr-code/?data=https%3A%2F%2Flabdhpurohit.github.io/Menu_Wave_Files/{email}/menuwave.html&size=300'''

    #------------------------
    #STORING LINK IN QR CODE
    #------------------------

    cursor = connection.cursor()
    cursor.execute(f"UPDATE users SET link = '{qr_data}' WHERE email = '{email}'")
    connection.commit()
    
    #------------------------
    #SENDING QR_CODE AND URL TO CONSUMER's EMAIL
    #------------------------

    sender_email = ""
    receiver_email = email
    password = ""
    message = MIMEMultipart("related")
    message["Subject"] = "Menu Card with QR Code"
    message["From"] = sender_email
    message["To"] = receiver_email


    # Email content
    email_content = f"""
    <html>
    <body>
        <h2>Menu Card</h2>
        <p>Dear Customer,</p>
        <p>Thank you for choosing MenuWave. Here is our menu card with a QR code:</p>
        <img src="{qr_data}">
        <p>You can scan the QR code or click the link below to access our menu online:</p>
        <a href="https://labdhpurohit.github.io/Menu_Wave_Files/{email}/menuwave.html">Menu Card</a>
        <p>Enjoy your meal!</p>
    </body>
    </html>
    """
    # Attach email content as HTML
    email_body = MIMEText(email_content, "html")
    message.attach(email_body)


    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", str(e))

    return render_template('home.html', show_element2=True, moutput="Menu Card Created Successfully")



#-------------------------------------
#-------------------------------------
#-------------------------------------
#END OF CHOOSING MENU
#-------------------------------------
#-------------------------------------
#------------------------------------- 


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------


#-------------------------------------
#-------------------------------------
#-------------------------------------
#START OF REDIRECTING LINKS
#-------------------------------------
#-------------------------------------
#-------------------------------------


#Sign In Page

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

#Sign Up Page

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html', show_element1=T, show_element2=F)

#Home Page

@app.route('/home2')
def home2():
    return render_template('home.html', show_element2=T, moutput="Menu Card Already Exist")


#Details Page
@app.route('/details')
def details():
    return render_template('details.html', show_element1=T)

@app.route('/forget_page')
def forget_page():
    return render_template('forget.html')

#-------------------------------------
#-------------------------------------
#-------------------------------------
#END OF REDIRECTING LINKS
#-------------------------------------
#-------------------------------------
#-------------------------------------

if __name__ == '__main__':
    app.run()#debug=False, host='0.0.0.0')



