from flask import render_template, request, redirect, send_file, flash, url_for,  session
from app import app

from .text_processing import Text_Analyze
from .files import temp_name, save_json, from_json, save_temp_xlsx, check_expiration, check_size
from .notations import Notations

descriptor = Notations()

def check_ext(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def check_lang():
    if 'language' in session.keys():
        return session['language']
    else:
        return 'RU'

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and check_ext(file.filename):
            flash(descriptor.translate(check_lang(),  'good_file'))
            return redirect(url_for('past'))
        elif not check_ext(file.filename):
            flash(descriptor.translate(check_lang(),  'bad_file'))
            return redirect(url_for('index'))
    notations = descriptor.make(check_lang(), 'base', 'index')
    about = { 'header': descriptor.translate(check_lang(),  'header'), 'info': descriptor.translate(check_lang(),  'info')}
    contains = render_template('index.html', about = about, notations = notations)
    return contains

@app.route('/past', methods = ['GET', 'POST'])
def past():
    notations = descriptor.make(check_lang(), 'base', 'past')
    if request.method == 'POST':
        if request.files:
            file = request.files['file']
            if file and check_ext(file.filename):
                flash(descriptor.translate(check_lang(),  'good_file'))
                text_blocks = [part.decode('utf-8') for part in file]
                return render_template('past.html', text_blocks = text_blocks, notations = notations)
        elif request.form:
            text = request.form['text']
            return render_template('past.html', text = text, notations = notations)
    contains = render_template('past.html', notations = notations)
    return contains

@app.route('/count', methods = ['GET', 'POST'])
def count():
    if request.method == 'POST':
        text = request.form['text']
        if not text:
            flash(descriptor.translate(check_lang(),  'no_text'))
            return redirect(url_for('index'))
        analized = Text_Analyze(text)
        all_data = {'General_data': descriptor.translate(check_lang(),  analized.general_data),
            'Word_frequency': descriptor.translate(check_lang(),  analized.words_analyzed),
            'POS_frequency': descriptor.translate(check_lang(),  analized.POS_analyzed)}
        if check_size(app.config['UPLOAD_FOLDER'], all_data, app.config['MAX_FILE_SIZE']):
            print(check_size(app.config['UPLOAD_FOLDER'], all_data))
            session['datafile'] = app.config['UPLOAD_FOLDER'] + '/' + temp_name('json')
            save_json(all_data, session['datafile'])
            download = True
        else:
            flash(descriptor.translate(check_lang(),  'big_download'))
        notations = descriptor.make(check_lang(), 'base', 'count')
        contains = render_template('count.html', general = analized.general_data,
            word_data = analized.words_analyzed,
            POS_data = analized.POS_analyzed,
            notations = notations, 
            download = download)
        return contains
    elif 'datafile' in session.keys():
        all_data = from_json(session['datafile'])
        notations = descriptor.make(check_lang(), 'base', 'count')
        download = True
        contains = render_template('count.html', general = all_data['General_data'],
            word_data = all_data['Word_frequency'],
            POS_data = all_data['POS_frequency'],
            notations = notations, 
            download = download)
        return contains
    else:
        return redirect(url_for('index'))
    
@app.route('/download')
def download():
    try:
        data = from_json(session['datafile'])
    except Exception as ex:
        print(f'The exception occured: {ex}')
    file = save_temp_xlsx(data)
    response = send_file(file.name, as_attachment=True, attachment_filename='results.xlsx')
    return response

@app.route('/lang_switch')
def language():
    try:
        if session['language'] == 'ENG':
            session['language'] = 'RU'
        else:
            session['language'] = 'ENG'
    except KeyError:
        session['language'] = 'ENG'
    return redirect(url_for('index'))

@app.route('/sestest')
def session_test():
    message = f"Session contains: {session.keys()}"
    if session.keys():
        for key in session.keys():
            message += f'\n {session[key]}'
    flash(message)
    return redirect(url_for('index'))

@app.route('/files')
def file_check_test():
    check_expiration(app.config['UPLOAD_FOLDER'])
    return redirect(url_for('index'))
    
@app.route('/startest', methods = ['GET', 'POST'])
def start():
    if request.method == 'POST':
        print(request.files.to_dict())
        print(request.form)
#        for item in dir(request):
#            if not item.startswith('_'):
#                try:
#                    print(request.__getattribute__(item))
#                except Exception as ex:
#                    print(f'Failed on getting the attribute "{item}" with exception {ex}')
    notations = descriptor.make(check_lang(), 'base')
    return render_template('index_test.html',  notations = notations)

@app.route('/startest2', methods = ['GET', 'POST'])
def _start():
    if request.method == 'POST':
        print(request.files['file'])
        print(request.files.to_dict())
        print(request.form)
    notations = descriptor.make(check_lang(), 'base')
    return render_template('index_test2.html',  notations = notations)
