#!/usr/bin/env ruby

require 'rubygems'
require 'mechanize'
require 'logger'
require 'open-uri'
require 'yaml'

# dbgen for google news
# most used:
# sports: http://news.google.com/?ned=us&topic=s
# world: http://news.google.com/?ned=us&topic=w
# entertainment: http://news.google.com/?ned=us&topic=e
# sci/tech: http://news.google.com/?ned=us&topic=t
# health: http://news.google.com/?ned=us&topic=m
# business: http://news.google.com/?ned=us&topic=b
# code from: http://zenmachine.wordpress.com/practical-text-classification-with-ruby/

tagSrc = {
    'sports' => 'http://news.google.com/?ned=us&topic=s',
    'world' => 'http://news.google.com/?ned=us&topic=w',
    'entertainment' => 'http://news.google.com/?ned=us&topic=e',
    'scitech' => 'http://news.google.com/?ned=us&topic=t',
    'health' => 'http://news.google.com/?ned=us&topic=m',
    'business' => 'http://news.google.com/?ned=us&topic=b'
}


limit=10

tagSrc.each do |tag,url|
    
    agent = WWW::Mechanize.new{ |obj| obj.log = Logger.new('dbgen.log') }
    puts("Start processing: #{url} for tag: #{tag}")
    
    news = Array.new
    page = agent.get(url)
    # snippet
    ni = page.search("div[@class='snippet']")
    ni.each do |n|
        news << n.to_s.gsub(/(<\/?[^>]*>)|(&(.+)\;)/,'')
    end
    
    File.open(tag+'.yaml', 'a+') { |f| f.puts news.to_yaml }
    puts("Done processing: #{url}")
end


