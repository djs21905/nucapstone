import os

dict = {'iPython':'ipython',
        'Pandas':'pandas',
        'Numpy': 'numpy',
        'nltk':'nltk',
        'Matplot': 'matplotlib',
        'Tensorflow': 'tensorflow',
        'keras':'keras', 
        'Scikit-learn':'scikit-learn'}

for k,v in dict.items():
    print('Installing %s'% k)
    os.system('py -m pip install %s' % v)
