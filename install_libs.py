#https://medium.com/@technoserviceclub/top-10-python-libraries-you-must-know-cc28a849c1fc
#https://pythontips.com/2013/07/30/20-python-libraries-you-cant-live-without/

import os

#Will need to install Build Tools for Visual Studio 2019 
#C++ 
#Link = https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2019

#Look into creating chocolatey script to install some of the following:
# SoundSwitch
# nmap
# wireshark
# steam
# chrome
# how to https://chocolatey.org/install



dict = {'Requests':'Requests',
        'Scrapy':'Scrapy',
        'BeautifulSoup':'beautifulsoup4',
        'Cython':'cython', 
        'Scikit':'scikit-learn',
        #'Twisted':'Twisted',
        'NumPy':'NumPy',
        'matplotlib':'matplotlib',
        'SciPy':'Scipy',
        'Scapy':'scapy', #Packet Sniffer https://scapy.net/
        'pywin32':'pywin32', #A python library which provides some useful methods and classes for interacting with windows.
        'EasyGUI':'easygui', #http://easygui.sourceforge.net/
        'Pandas':'pandas',
        'Virtual Environment':'virtualenv',
        'keras':'keras',
        'nltk':'nltk',
        'seaborn':'seaborn',
        'gensim':'gensim',
        'spyder':'spyder',
        'jupyterlab':'jupyterlab'
        }

#Add later
# keras, tensorflow, nltk, seaborn, gensim
#spyder, jupyterlab
#

for k,v in dict.items():
    print('Installing %s'% k)
    os.system('py -m pip install %s' % v)


#Install Libraries
#import pip
#installed_packages = pip.get_installed_distributions()
#installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
#print(installed_packages_list)
#sorted(["%s==%s" % (i.key, i.version) for i in pip.get_installed_distributions()])