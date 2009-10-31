#!/usr/bin/env ruby
# code from: http://zenmachine.wordpress.com/practical-text-classification-with-ruby/
# patch for classifier: 
# http://rubyforge.org/tracker/index.php?func=detail&aid=17839&group_id=655&atid=2587
#

require 'rss/1.0'
require 'rss/2.0'
require 'rubygems'
require 'mechanize'
require 'logger'
require 'open-uri'
require 'stemmer'
require 'classifier'
require 'yaml'
require 'crm114'
require 'bishop'




class NewsClassifier
    @bayesianClassifier=nil
    @lsiClassifier=nil
    @crm114Classifier=nil
    @bishopClassifier=nil
    
    @sports=@world=@entertainment=@scitech=@health=@business=nil
    
    def loadTrainingFiles
        @sports=YAML::load_file('sports.yaml')
        @world=YAML::load_file('world.yaml')
        @entertainment=YAML::load_file('entertainment.yaml')
        @scitech=YAML::load_file('scitech.yaml')
        @health=YAML::load_file('health.yaml')
        @business=YAML::load_file('business.yaml')
    end
    
    def trainBayesClassifier
        @bayesianClassifier = Classifier::Bayes.new('sports', 'world','entertainment','scitech','health','business')
        
        @sports.each { |s| @bayesianClassifier.train_sports s }
        @world.each { |w| @bayesianClassifier.train_world w }
        @entertainment.each { |e| @bayesianClassifier.train_entertainment e }
        @scitech.each { |s| @bayesianClassifier.train_scitech s }
        @health.each { |h| @bayesianClassifier.train_health h }
        @business.each { |b| @bayesianClassifier.train_business b }
    end

    def trainLSIClassifier
        # lsi needs a fix for the newest GSL. see http://rubyforge.org/forum/forum.php?thread_id=10069&forum_id=2816
        @lsiClassifier = Classifier::LSI.new :auto_rebuild => false
               
        @sports.each { |s| @lsiClassifier.add_item(s, "Sports") }
        @world.each { |w| @lsiClassifier.add_item(w,"World") }
        @entertainment.each { |e| @lsiClassifier.add_item(e,"Entertainment") }
        @scitech.each { |s| @lsiClassifier.add_item(s,"Scitech") }
        @health.each { |h| @lsiClassifier.add_item(h,"Health") }
        @business.each { |b| @lsiClassifier.add_item(b,"Business") }
        # no auto index building
        @lsiClassifier.build_index
    end
    
    def trainCRM114Classifier
        @crm114Classifier=Classifier::CRM114.new(["Sports", "World","Entertainment","Scitech","Health","Business"])
        
        @sports.each { |s| @crm114Classifier.learn!("Sports",s) }
        @world.each { |w| @crm114Classifier.learn!("World",w) }
        @entertainment.each { |e| @crm114Classifier.learn!("Entertainment",e) }
        @scitech.each { |s| @crm114Classifier.learn!("Scitech",s) }
        @health.each { |h| @crm114Classifier.learn!("Health",h) }
        @business.each { |b| @crm114Classifier.learn!("Business",b) }
        
    end
    
    def trainBishopBayesClassifier
        @bishopClassifier = Bishop::Bayes.new #('sports', 'world','entertainment','scitech','health','business')
        
        @sports.each { |s| @bishopClassifier.train("sports",s) }
        @world.each { |w| @bishopClassifier.train("world",w) }
        @entertainment.each { |e| @bishopClassifier.train("entertainment",e) }
        @scitech.each { |s| @bishopClassifier.train("scitech",s) }
        @health.each { |h| @bishopClassifier.train("health",h) }
        @business.each { |b| @bishopClassifier.train("business",b) }
    end

    def getBishopResult(t)
        res=@bishopClassifier.guess(t)
        results = res.sort_by{|score| -score.last }
        return results.first[0].capitalize if not results.nil? 
#	puts t
    end
    def initialize
        loadTrainingFiles
        
        trainBayesClassifier
        trainLSIClassifier
        #trainCRM114Classifier
        trainBishopBayesClassifier
    end
    
    def runTest 

        rssURL = "http://rss.news.yahoo.com/rss/topstories" 
        agent = WWW::Mechanize.new { |obj| obj.log = Logger.new('news_classifier.log') }
        rssBody = agent.get_file(rssURL)
        
        rss = RSS::Parser.parse(rssBody.to_s, false)
        print "link,bayesian,LSI,bishop,CRM114\n"    
        rss.channel.items.each do  |r|
            t=r.description.to_s.gsub(/(<\/?[^>]*>)|(&(.+)\;)/,'')
            print "#{r.link}: #{@bayesianClassifier.classify(t)},"
            print "#{@lsiClassifier.classify(t)}, "
            print "#{getBishopResult(t)},\n"
            
            #,#{@crm114Classifier.classify.first}\n"
        end
    end
end


# main
nc = NewsClassifier.new
nc.runTest






