🚀 NeuroScript 2.0 — Installation Guide
1️⃣ Clone the repository

First, download the project from GitHub:

git clone https://github.com/Daniel321W/NeuroScript2.0.git
2️⃣ Create a virtual environment

Go to the project directory:

cd NeuroScript2.0

Create a virtual environment:

python -m venv venv
3️⃣ Activate the virtual environment
🪟 Windows
PowerShell
venv\Scripts\Activate.ps1
CMD
venv\Scripts\Activate.bat
🐧 Linux
source venv/bin/activate
4️⃣ Install required dependencies

After activating the environment, install all required libraries:

pip install -r requirements.txt
5️⃣ Run the application

Start the development server:

python manage.py runserver

The application should now be available at:

http://localhost:8000/accounts/login/
⚠️ Fix for gobject-2.0-0 Error (Windows)

If you encounter the following error:

OSError: cannot load library 'gobject-2.0-0'

follow these steps.

Install MSYS2

Download and install MSYS2:

👉 https://www.msys2.org/

Install required package

Open the MSYS2 terminal and run:

pacman -S mingw-w64-x86_64-pango

Press Enter to confirm installation.

Add MSYS2 to PATH

Add the following directory to your system PATH:

C:\msys64\mingw64\bin
Restart your computer

After restarting:

Activate the virtual environment again
Run the server
python manage.py runserver
✅ Done

Your NeuroScript 2.0 application should now work correctly.
