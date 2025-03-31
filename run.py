from website import create_app

app = create_app()

if __name__ == '__main__':
    #when runing the app all changes will be updated
    app.run(host ='0.0.0.0',debug=True,port=5000)
