#!/usr/bin/env python

import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


class User(ndb.Model):
    """Sub model for representing a user."""
    email = ndb.StringProperty(indexed=True)
    receiveEmail = ndb.BooleanProperty(default=True)
    loginCount = ndb.IntegerProperty(default=0)

class Page(webapp2.RequestHandler):
    def templateValues(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Profile'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login / Sign Up'
        return {
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
        if not users.get_current_user() or not users.is_current_user_admin():
            self.redirect("/")
            return
        templateValues = self.templateValues()
        query = User.query()
        all_users = query.fetch()
        templateValues["all_users"] = all_users
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(templateValues))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/admin.html').render(templateValues))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))


class Profile(Page):        
    def get(self):
        receiveEmail = self.request.get('receiveEmail')
        user = users.get_current_user()
        templateValues = self.templateValues()
        if user:
            siteUser = User.get_or_insert(user.email())
            siteUser.email = user.email()
            siteUser.loginCount = siteUser.loginCount + 1
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

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/profile', Profile),
    ('/reading', Reading),
    ('/news', News),
    ('/experiments', Experiments),
    ('/brainstorming', Brainstorming),
    ('/fundraising', Fundraising),
    ('/admin', Admin),
], debug=True)
