from flask import Flask,render_template,request
import re

app = Flask(__name__)


import re
def FormValidation(q):
    pattern = r'^<(([A-E]:0.(\d+))|([A-E]))((;[A-E]:0.(\d+))|(;[A-E])){0,}>$'  
    r = re.match(pattern,q)
    
    if not r:
        return 'Invalid Query'
    else:
        return ''

def StatModel(q):
    import os
    import numpy as np
    files = os.listdir("Statistical Model/Docs")
    
    r = {}
    C = ['A','B','C','D','E']
    for d in files:
        
        x =[]
        f = open('Statistical Model/Docs/'+d,'r')
        s = f.read()
        f.close()
        
        for c in C:
            x.append(s.count(c))
        x = np.array(x)
        r[d]= np.array(np.divide(x,np.sum(x)))
    q = q.strip('<>')
    q = q.split(';')
    Q = [0,0,0,0,0]
    for w in q:
        if len(w) == 1:
            Q[ord(w)-ord('A')] = 1
        else:
            Q[ord(w[0])-ord('A')] = float(w[2:])
    res = {}
    for k,v in r.items():
        res[k] = round(np.sum(np.multiply(v,Q)),2)
    
    return sorted(res.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    
        
           
        



@app.route('/', methods=['GET','POST'])
def form():
    if request.method == 'POST'  :
        
        # print(error)
        query = request.form['query']
        error = FormValidation(query)
        if error :
            return render_template('form.html',error=error,query=query)
        else:
            r = StatModel(query)
            
            return render_template('form.html',error='',query=query,r=r)
        
    return render_template('form.html',error='',query='',r=[])



if __name__ == '__main__':
    app.run(debug = True)

