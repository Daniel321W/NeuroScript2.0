HOW TO RUN?

Download project via following command:

git clone https://github.com/Daniel321W/NeuroScript2.0.git

Then, go to the location where your project is located and run command in NeuroScript2.0/

python -m venv venv

And run virtual enviornment using command:

ON WINDOWS

venv\Scripts\Activate.ps1 (in PS)
venv\Scripts\Activate.bat (in CMD)

ON LINUX

source venv/bin/activate

Once your environment has been activated - you can install all required libraries by following command:

pip install -r requirements.txt

And launch app using:

python manage.py runserver

if following error occured:

OSError: cannot load library 'gobject-2.0-0': error 0x7e.  Additionally, ctypes.util.find_library() did not manage to locate a library called 'gobject-2.0-0'

1. download msys2 from https://www.msys2.org/
2. install application
3. run app
4. put following command: pacman -S mingw-w64-x86_64-pango
5. put enter
6. Then 
