#!/usr/bin/env ruby
require 'rubygems'
require 'ferret'
require 'find'
include Ferret
# code from: http://zenmachine.wordpress.com/ferret-indexing-with-ruby/
# as an exercise, implement a search using wikipedia articles.
# download the file http://download.wikimedia.org/ptwiki/latest/ptwiki-latest-pages-articles.xml.bz2
# or http://download.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2 if you are willing to
# test it using english language (warning, this file is almost 6Gb as of now...)
# you got to split each article, which is easy under ruby or python. 
# create a file structure which may reflect the current wikipedia site, or separate them by category

index = Index::Index.new(:default_field => 'content', :path => './ferret-test', :analyzer => Analysis::WhiteSpaceAnalyzer.new)


ini = Time.now
numFiles=0

Find.find("./linux-2.6.23.1/") do |path|
	puts "Indexing: #{path}"

	numFiles=numFiles+1

	if FileTest.file? path
		File.open(path) do |file|

			index.add_document(:file => path, :content => file.readlines)
		end
	end
end

elapsed = Time.now - ini

puts "Files: #{numFiles}"

puts "Elapsed time: #{elapsed} secs\n"
