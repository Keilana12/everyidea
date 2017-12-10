#!/usr/bin/env python

import os

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

# jinja is a framework for templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]


class User(ndb.Model):
    """Sub model for representing a user."""
    email = ndb.StringProperty(indexed=True)
    receiveEmail = ndb.BooleanProperty(default=True)
    loginCount = ndb.IntegerProperty(default=0)

class Page(webapp2.RequestHandler):
    def templateValues(self):
        #admin, profile/login, for every page
        user = users.get_current_user()
        if user:
            is_admin = users.is_current_user_admin()
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Profile'
        else:
            is_admin = False
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login / Sign Up'
        return {
            'is_admin': is_admin,
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'self_url': self.request.uri
        }

class Home(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/index.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))
        
class Admin(Page):
    def get(self):
        #if not admin go to home page
        if not users.get_current_user() or not users.is_current_user_admin():
            self.redirect("/")
            return
        templateValues = self.templateValues()
        all_users = User.query().fetch()
        templateValues["all_users"] = all_users
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(templateValues))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/admin.html').render(templateValues))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))


class Profile(Page):        
    def get(self):
        #if user clicks enable/disable emails then variable will either have Enable or Disable
        receiveEmail = self.request.get('receiveEmail')
        user = users.get_current_user()
        templateValues = self.templateValues()
        if user:
            siteUser = User.get_or_insert(user.email())
            siteUser.email = user.email()
            #todo: fix login count to true login count
            siteUser.loginCount = siteUser.loginCount + 1
            #put= save  to database
            siteUser.put()
            if receiveEmail == 'Enable' or receiveEmail == 'Disable':
                if receiveEmail == 'Enable':
                    siteUser.receiveEmail = True
                elif receiveEmail == 'Disable':
                    siteUser.receiveEmail = False
                siteUser.put()
                self.redirect("/profile")
                return
            elif siteUser.receiveEmail:
                opt_value = "Disable"
            else:
                opt_value = "Enable"
            templateValues["receiveEmail"] = siteUser.receiveEmail
            templateValues["opt_value"] = opt_value
            
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(templateValues))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/profile.html').render(templateValues))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class Reading(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/reading.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class News(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/news.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class Experiments(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/experiments.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class Brainstorming(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/brainstorming.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class Fundraising(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/fundraising.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))
        
class Experiment1(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/experiment1.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))
        
class Experiment2(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/experiment2.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))
        
class Information(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/information.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/profile', Profile),
    ('/reading', Reading),
    ('/news', News),
    ('/experiments', Experiments),
    ('/brainstorming', Brainstorming),
    ('/fundraising', Fundraising),
    ('/admin', Admin),
    ('/experiment1', Experiment1),
    ('/experiment2', Experiment2),
    ('/information', Information),
], debug=True)
