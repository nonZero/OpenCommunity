@echo off

echo Installing Pillow (PIL)
easy_install pillow==3.2.0

echo ===============================
echo Installing win-psycopg
easy_install http://www.stickpeople.com/projects/python/win-psycopg/2.6.1/psycopg2-2.6.1.win32-py2.7-pg9.4.4-release.exe

rem echo ===============================
rem echo Installing lxml
rem easy_install lxml==2.3

echo ===============================
echo Installing pycrypto
easy_install http://www.voidspace.org.uk/python/pycrypto-2.6.1/pycrypto-2.6.1.win32-py2.7.exe
rem echo lxml
