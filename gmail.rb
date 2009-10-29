#!/usr/bin/env ruby
# code from: http://zenmachine.wordpress.com/2007/11/11/scraping-with-firebug-and-wwwmechanize/

require 'rubygems'
require 'mechanize'
require 'logger'

agent = WWW::Mechanize.new { |obj| obj.log = Logger.new('gmail.log') }

page = agent.get('https://www.gmail.com')

form = page.forms.first
form.Email = ''
form.Passwd = ''

page = agent.submit(form)

page = agent.get('http://mail.google.com/mail/contacts/data/export?exportType=ALL&groupToExport=&out=OUTLOOK_CSV')

page.save_as('gmail_contacts.csv')

