from website import create_app #website is a python package it will by default run all of the stuff in init.py

app=create_app()

if __name__=='__main__': #only if we run this file, the line will be executed
    app.run(debug=True) #everytime we change to the code the webserver will rerun
    