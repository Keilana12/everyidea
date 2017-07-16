## Description

everyidea is a website originally created by Isabelle Rugg to promote education
and crowdsourced idea generation related to some of the problems the world faces
today.  It is a collaborative effort with several contributors.

## Technologies used:

* Google Domains - a domain registrar that redirects everyidea.net to the
appropriate place
* Google AppEngine - a cloud hosting site that runs the code
* Google Datastore - the database used to store information like user profiles
* Python - a programming language that is good to learn with
* Java - a programming language that is necessary for eclipse even though we
aren't going to use it at all
* Git - pulling new changes from origin and pushing improvements added by you
* GitHub - a website that stores our changes
* GitHub Desktop - an application on the computer that communicates with the
website in the cloud and lets us push and pull the improvements
* HTML - a simple programming language that browsers can understand to display
web pages
* CSS - a programming language that is the visual side of HTML and styles the
page
* Jinja2 - python framework to define what piece of code is called for each url
* Eclipse
* PyDev

## Setup Instructions:

1. This [site](https://cloud.google.com/appengine/docs/standard/python/tools/setting-up-eclipse) has a pretty good step by step guide for setting up the basics.
  * When it tells you to check python version you can open a terminal to do this.
  * When installing the pydev plugin, be sure and select the entry when it asks
  you if you trust these certificates (by default it is not selected and isn't
  obvious).  

1. Download and install [GitHub Desktop](https://desktop.github.com)
   once opened, either sign in or create a free account
   
1. Clone the everyidea repository to your computer.
   1. click on 'Clone a Repository'
   1. use url: ikrocks/everyidea
   1. change the local path to be in your eclipse workspace.  This should be
      something like /Users/jsmith/eclipse-workspace/everyidea

1. In Eclipse create the project
   1. Select File->New->Project...
   1. Select PyDev->PyDev Google App Engine Project
   1. Use everyidea as the project name.  It should tell you that the location
      already contains python files and that the project will include them.
   1. When it asks for the Google App Engine Directory, type in
      /usr/local/google_appengine.  If you hit 'Browse' instead of typing it in
      directly, it is much harder to select this directory.
  
1. Test the application locally
   1. Right click on the everyidea project in the package explorer
   1. Select Run As -> PyDev: Google App Run
   1. This will bring up the console and may ask you if you want to allow checks
      for update on startup.  Either Y or N is fine.
   1. Open up [http://localhost:8080](http://localhost:8080) in a browser.
   1. If you choose to Login, you can use any email you want.  If you select the
      checkbox to login as administrator, then you will see an extra Admin page.
  
1. Test that you can check in changes
   1. In eclipse, open the TEST.TXT file.
   1. Make changes to the file.
   1. In GitHub Desktop, you should see 1 changed files.
   1. Add a short summary and click 'Commit to master'.
   1. In the upper right hand corner click 'Push origin'
   1. If you get an authentication failed error, this means that your github user
      has not yet been added to the project.  Contact admin@everyidea.net
      (Isabelle) to get added.