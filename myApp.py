from flask import Flask,render_template,jsonify,request,redirect,url_for,session
from tinydb import TinyDB,Query
import time , datetime
app = Flask(__name__)
app.secret_key = "welcome to my kingdom"
@app.route('/',methods=['POST','GET'])
def signUP_page():
	if request.method=='POST':
		text=request.form['aid']
		passwd=request.form['password']
		mapper={'0':'h', '1':'i', '2':'j', '3':'k', '4':'l', '5':'m', '6':'n', '7':'o', '8':'p', '9':'q', 'a':'t', 'A':'t'}
		temp=''
		for i in text:
			if (i in mapper):
				temp = temp+mapper[i]
		db=TinyDB('username.json')
		Object = Query()
		resp=db.search(Object.AID == temp)
		print(resp)
		if len(resp)==1 and passwd.lower()=='12345':
			session['secret_msg']='power'
			session['username']=resp[0]['name']
			return redirect(url_for('second_page'))
		else:
			msg="Invalid credentials"
		return msg
	else:
		return render_template('index1.html')
@app.route('/welcome_page')
def second_page():
	if 'secret_msg' in session:
		if session["secret_msg"]=='power':
			return "welcome to my page ,"+session['username']+"  <br> <a href='/logout'>click here to logout </a>"
	else:
		return redirect(url_for('signUP_page'))
@app.route('/logout')
def logout_page():
	if 'secret_msg' in session:
		session.pop('secret_msg', None)
		return redirect(url_for('signUP_page'))
@app.route('/update_comment')
def comment_page():
	db = TinyDB('comments.json')
	if len(db.all())==0:
		return render_template('comment.html')
	else:
		return render_template('comment.html',data=db.all()[::-1])
@app.route('/insert_comment')
def update_comment():
	text=request.args.get('comment')
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print(text)
	db = TinyDB('comments.json')
	#need to make AID dynamic
	db.insert({'comment': text, 'AID': 'A611250', 'timestamp': st})
	data={"response":"thank you for your feedback"}
	return jsonify(data)
if __name__ == '__main__':
   app.run(debug = True)