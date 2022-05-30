from frontend import init_app

flaskapp = init_app()

if __name__ == '__main__':
    flaskapp.run(debug=True)