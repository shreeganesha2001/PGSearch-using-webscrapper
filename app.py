from flask import Flask, render_template, request
from autoscraper import AutoScraper
import pandas as pd
import time
app = Flask(__name__)

#creating object and loading
pg_scraper = AutoScraper()
pg_scraper.load('pg_search')    
    
@app.route("/",methods=['GET'])  
def home():    

    #when user search it
    if request.args.get('search'):
        #inputs
        search = request.args.get('search')
        
        #call function to retrieve data
        search_data,original_url = searchquery(search)
        data_length = len(search_data)
        
        #show to user
        return render_template("index.html",data = {'query':search,'searchData':search_data,'totalRecords':data_length}) 
    
    #default data_length when no search
    data_length = -1
    return render_template("index.html",data = {'query':"",'searchData':"",'totalRecords':data_length}) 
def searchquery(search):
    #load library    

    #define url
    pg_url="https://www.google.com/search?rlz=1C1CHBD_en__901__901&tbs=lf:1,lf_ui:2&tbm=lcl&sxsrf=AB5stBiGy60-3CeYwVM0YJOVeQcIxzK4ig:1689344550694&q=pg+near+{}&rflfq=1&num=10&ved=2ahUKEwic2OLuso6AAxUzSmwGHf4XBbsQtgN6BAg9EAI#rlfi=hd:;si:;mv:[[12.9827447,77.64691619999999],[12.966947099999999,77.6304273]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2".format(search)    
    
    #get data
    data = pg_scraper.get_result_similar(pg_url, group_by_alias=True)

    #combine data into tuple to show it to user
    search_data = tuple(zip(data['Name'],data['Address'],data['Phone'],data['Rating']))

    #creating dataframe so that user can download it in csv format
    df = pd.DataFrame(columns=['Query','Name','Address','Phone','Rating'])
    for i in range(len(search_data)):
        df.loc[len(df)] = [search,search_data[i][0],search_data[i][2],search_data[i][1],search_data[i][3]]
    df.to_csv("static/searchedData.csv",index=False)
    
    #returing data
    return search_data,pg_url
if __name__ == "__main__":
    app.run(debug=True)
