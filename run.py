from __init__ import app, db
import views

if __name__ == "__main__":
    db.create_all()
    app.run(port=8000, debug=True)
