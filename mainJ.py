from flask import Flask, render_template, request, redirect, url_for

import shelve
from RecordJ import RecordJ
from AddRecordFormJ import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homeJ.html')

@app.route('/recordJ', methods=['GET', 'POST'])
def recordJ():
    form = AddRecordFormJ(request.form)
    print('The method is ' + request.method)
    if request.method == 'POST':
        if form.validate() == False:
            print('All fields are required.')
        else:
            recordList = {}
            db = shelve.open('storage.db', 'c')
            try:
                recordList = db['Records']
            except:
                print("fail to open database")
            new_record = RecordJ(form.date_redeemed.data, form.item_redeemed.data,form.receipt.data)
            recordList[new_record.get_id()] = new_record
            db['Records'] = recordList
            db.close()
            return redirect(url_for('summary'))

    return render_template('recordJ.html', form=form)

@app.route('/summary2')
def summary():



    dictionary = {}
    db = shelve.open('storage.db', 'r')
    dictionary = db['Records']
    db.close()

    # convert dictionry to list
    list = []
    for key in dictionary:
        item = dictionary.get(key)
        #print("here: ", user.get_userID())
        #print("here:", user.get_firstname())
        list.append(item)

    return render_template('summary2J.html', records=list, count=len(list))


if __name__ == "__main__":
    app.run()