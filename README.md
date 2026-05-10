HOW TO RUN?

STEP 1
Download project via following command:

git clone https://github.com/Daniel321W/NeuroScript2.0.git

STEP 2
Then, go to the location where your project is located and run command in NeuroScript2.0/

python -m venv venv

STEP 3
And run virtual enviornment using command:

ON WINDOWS

venv\Scripts\Activate.ps1 (in PS)
venv\Scripts\Activate.bat (in CMD)

ON LINUX

source venv/bin/activate

STEP 4
Once your environment has been activated - you can install all required libraries by following command:

pip install -r requirements.txt

STEP 5
And launch app using:

python manage.py runserver (your service should be available under: http://localhost:8000/accounts/login/)

In case of following error:

OSError: cannot load library 'gobject-2.0-0': error 0x7e.  Additionally, ctypes.util.find_library() did not manage to locate a library called 'gobject-2.0-0'

1. download msys2 from https://www.msys2.org/
2. install application
3. run app
4. put following command: pacman -S mingw-w64-x86_64-pango
5. put enter
6. Then add this path to your env PATH: "C:\msys64\mingw64\bin"
7. restart your pc
8. Try again (go back to STEP 3)
