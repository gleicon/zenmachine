#!/usr/bin/env ruby
require 'rubygems'
require 'ferret'
require 'find'
# code from: http://zenmachine.wordpress.com/ferret-indexing-with-ruby/

wot = ARGV[0]
if wot.nil?
	puts "use: search.rb <query>"
	exit
end


index = Ferret::Index::Index.new(:default_field => 'content', :path => './ferret-test', :analyzer => Ferret::Analysis::WhiteSpaceAnalyzer.new)


ini = Time.now

puts "Searching"


docs=0

# uncomment line below for 10 first results, and comment the subsequent line.

index.search_each(wot) do |doc, score| 
#index.search_each(wot, options={:limit=>:all}) do |doc, score|
	puts index[doc]['file'] + " score: "+score.to_s
	docs+=1
end


elapsed = Time.now - ini

puts "Elapsed time: #{elapsed} secs\n"

puts "Documents found: #{docs}"

