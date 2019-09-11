from flask import Flask, render_template, redirect
import scraped_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)


client = pymongo.MongoClient()
db = client.mars_db
collection = db.marsinfo



@app.route('/scrape')
def scrape():
    mars = scraped_mars.scrape()    
    db.marsinfo.insert_one(mars)
    db.marsinfo.update({}, mars, upsert=True)
    
    return redirect('/', code=302)

@app.route("/")
def index():
    mars = db.marsinfo.find_one()
    return render_template("index.html", mars = mars)


if __name__ == "__main__":
    app.run(debug=True)


