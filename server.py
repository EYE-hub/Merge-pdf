# -*- coding: utf-8 -*-
from flask import Flask, flash, render_template,  request, redirect, send_file
from flask import send_from_directory
import PyPDF2


UPLOAD_FOLDER = './upload_files'
ALLOWED_EXTENSIONS = set({'pdf'})

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = "imconfused"

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/merge.html', methods=['POST'])
def upload_file():

	if request.method == 'POST':
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
	files = request.files.getlist('files[]')
	for file in files:
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
		# 	filename = secure_filename(file.filename)
		# 	file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			flash('File(s) successfully uploaded')	
			pdf_combiner(files)
			# return_file()
			# delete()
		if not allowed_file(file.filename):
			flash('File is not in PDF format')
	
	
	return render_template('merge.html') 


	
@app.route('/return-file1')
def return_file1():	
		return send_file("./watermarked.pdf")
		


def pdf_combiner(pdf_list):
	merger = PyPDF2.PdfFileMerger()
	for pdf in  pdf_list:
		print(pdf)
		merger.append(pdf)
	merger.write('super_file.pdf')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)


@app.route('/')
def my_home():
	return render_template('merge.html')



if __name__ == "__main__":
    app.run(debug=True)
