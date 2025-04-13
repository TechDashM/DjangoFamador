# DjangoFamador
For Educational Purpose Only

Instruction on how to run the Django Project

#Open your VSCODE then open Terminal
In terminal Type these (each line must be executed first before moving another line and after '#' is for comments only not for execution)
cd FamadorDjango



# Virtual Environment is not created
for Windows
python -m venv venv 
For Linux 
python3 -m venv venv



# Activate Virtual Environment
 Windows:
venv\Scripts\activate
 Mac/Linux:
source venv/bin/activate



# For downloading Modules for the django
pip install -r requirement.txt 



# Run Migrations
python manage.py migrate



# Create Superuser (OPTIONAL)
# username, email,password (the password is hidden when you type)
python manage.py createsuperuser


# Run Development Server
python manage.py runserver



# Then after go to any website app (Chrone, Brave, Firefox) then copy paste this
http://127.0.0.1:8000/


all done


  
 
