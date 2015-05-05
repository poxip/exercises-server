from exercises import app

@app.route('/')
def index():
    return 'Yello!'