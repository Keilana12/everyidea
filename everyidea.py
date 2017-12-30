#!/usr/bin/env python

import os

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
from __builtin__ import True

# jinja is a framework for templates
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

class Comment(ndb.Model):
    """Sub model for representing comments."""
    author = ndb.StringProperty(indexed=True)
    page = ndb.StringProperty(indexed=True)
    text = ndb.StringProperty()
    isApproved = ndb.BooleanProperty(indexed=True, default=False)

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
        action = self.request.get('action')
        if (action == "approve"):
            author = self.request.get('author')
            page = self.request.get('page')
            query = Comment.query(Comment.page == page and Comment.author == author)
            for each in query.fetch():
                each.isApproved = True
                each.put()
        if (action == "unapprove"):
            author = self.request.get('author')
            page = self.request.get('page')
            query = Comment.query(Comment.page == page and Comment.author == author)
            for each in query.fetch():
                each.isApproved = False
                each.put()
        templateValues = self.templateValues()
        all_users = User.query().fetch()
        templateValues["all_users"] = all_users
        all_comments = Comment.query().fetch()
        templateValues["all_comments"] = all_comments
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


class Fundraising(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/fundraising.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))
        
class WaterShortage(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/water_shortage/home.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class WaterShortageNews(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/water_shortage/news.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class WaterShortageExperiments(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/water_shortage/experiments.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class WaterShortageExperiment1(Page):
    def get(self):
        commentText = self.request.get('commentText')
        user = users.get_current_user()
        templateValues = self.templateValues()
        templateValues["commentPage"] = "/water_shortage/experiment1"

        if user:
            siteUser = User.get_or_insert(user.email())
            siteUser.email = user.email()
            siteUser.put()
            comment = Comment.get_or_insert("WaterShortageExperiment1_"+ siteUser.email)
            comment.author = siteUser.email
            comment.page = "WaterShortageExperiment1" 
            if commentText:
                comment.text = commentText
            if comment.text:
                comment.isApproved = False
                comment.put()
                templateValues["submitText"] = "Update Comment"
            else:
                templateValues["submitText"] = "Add Comment"
            templateValues["comment"] = comment

        query = Comment.query(Comment.page == "WaterShortageExperiment1")
        templateValues["comments"] = query.fetch()

        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(templateValues))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/water_shortage/experiment1.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/comments.html').render(templateValues))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))
        
class WaterShortageExperiment2(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/water_shortage/experiment2.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class WaterShortageBrainstorming(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/water_shortage/brainstorming.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

class GlobalWarming(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/global_warming/home.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))


# not used yet
class Reading(Page):
    def get(self):
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/header.html').render(self.templateValues()))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/reading.html').render({}))
        self.response.write(JINJA_ENVIRONMENT.get_template('pages/footer.html').render({}))

app = webapp2.WSGIApplication([
    ('/', Home),
    ('/global_warming', GlobalWarming),
    ('/water_shortage', WaterShortage),
    ('/reading', Reading),
    ('/water_shortage/news', WaterShortageNews),
    ('/water_shortage/experiments', WaterShortageExperiments),
    ('/water_shortage/experiment1', WaterShortageExperiment1),
    ('/water_shortage/experiment2', WaterShortageExperiment2),
    ('/water_shortage/brainstorming', WaterShortageBrainstorming),
    ('/profile', Profile),
    ('/fundraising', Fundraising),
    ('/admin', Admin),
], debug=True)
