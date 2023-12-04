from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import pandas as pd

app = Flask(__name__, template_folder="templates")                 #initializing the app

database_file = 'product_db.db'

with sqlite3.connect(database_file) as con:                        #initialize the sql script with the desired file name
    with open('init_script.sql','r') as f:
        commands = f.read()
        con.executescript(commands)
        con.commit()

@app.route('/')                                                    #home route returns the home page template
def home():
    return render_template("base.html")

@app.route('/data_entry/')                                         #entry route returns the data entry page template
def entry():
    return render_template("entry.html", title='data entry')

@app.route('/retreive_data')                                       #retieve route returns the search page template
def retrieve():
    return render_template("search.html")

@app.route('/data_form/', methods = ['POST'])                      #handleDate method is used to process that user entered data
def handleData():
    product_category = request.form.get("product_category")        #getting all form data and assigning to variables
    product_description = request.form.get("product_description")
    price = request.form.get("price")
    product_code = request.form.get("product_code")

    with sqlite3.connect(database_file) as con:                    #entering all form data into the sql database
        command = 'INSERT INTO  product (product_category, product_description, price, product_code) VALUES(?,?,?,?)'
        parameters = (product_category, product_description, price, product_code)
        con.execute(command, parameters)
    return redirect(url_for('home'))                               #takes the use back to the home page after they hit submit

@app.route('/search_results/', methods = ['POST'])                 #results function controls the method for displaying product search results                                 
def results():
    category_search = request.form.get("category_search")          #storing the user's category search value

    with sqlite3.connect(database_file) as con:                    #converting the sql database to a pandas dataframe       
        df = pd.read_sql('SELECT * from product', con)
    
    df['price'] = df['price'].apply(lambda x: '${}'.format(x))     #formating the price column so that there is a '$' in front of all values

    if category_search is not None:                                #if the search value exists returning the dataframe rows where the product category matches the user's search value, ignoring case and NA values 
        return_df = df[df['product_category'].str.contains(category_search, case=False, na=False)]
    else:
        return_df = df                                             #if there is no user search value, simply return the original entire dataframe 
        
    
    return render_template('view_products.html',df = return_df)    #return the page template for view products and the correct dataframe




if __name__ == '__main__':
    app.run(debug=True)




