from textprocessing import *

from django.shortcuts import render
from django.shortcuts import redirect
import os
jn = os.path.join

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

# Load models:
root = os.path.split(os.getcwd())[0]
# Load:
with open(jn(root, 'artifacts', 'models', 'countvec.pkl'), 'rb') as fs:
    countvec = pickle.load(fs)
with open(jn(root, 'artifacts', 'models', 'lda.pkl'), 'rb') as fs:
    lda = pickle.load(fs)

predictor = Predictor(countvec, lda)

# Returns home page:
def index(request, *args):
    # Have I been redirected from user input?
    old_post = request.session.get('_old_post')
    print(os.path.isdir(root + '/artifacts'))

    if old_post is not None:        
        # Retrieve input value:
        input_value = request.session.get('_old_post').get('input_tweet')

        # Create output value:
        output = predictor.predict(input_value)

        # Finally, remove post request from session: 
        request.session.pop('_old_post')

        return render(request, 'index_response.html', {'title': output})
        
    # Regular home page:
    if request.method == "GET":
        return render(request, 'index.html')
    

# Processes user input:
def action(request):
    # Add user input to request session:
    if len(request.POST.get('input_tweet')) > 0:
        request.session['_old_post'] = request.POST
    return redirect(index)
