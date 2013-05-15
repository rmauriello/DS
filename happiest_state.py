import sys
import json
import string
import re
import codecs
import operator
    

states = ["AL",  "AK",  "AZ",  "AR",  "CA",  "CO",  "CT",  "DE",  "FL",  "GA",  "HI",  "ID",  "IL",  "IN",  "IA",  "KS",  "KY",  "LA",  "ME",  "MD",  "MA",  "MI",  "MN",  "MS",  "MO",  "MT",  "NE",  "NV",  "NH",  "NJ",  "NM",  "NY",  "NC",  "ND",  "OH",  "OK",  "OR",  "PA",  "RI",  "SC",  "SD",  "TN",  "TX",  "UT",  "VT",  "VA", \
 "WA",  "WV",  "WI",  "WY"]


def parse_tweets(t):
    data = []
    deleted_tweets = 0
    for line in t:    
        filter(lambda x: x in string.printable, line)
        if re.match(r'^{"delete".*',line):
            deleted_tweets += 1
            next
        else:
            data.append(json.loads(line))

#    print "Deleted tweets - %d" % deleted_tweets
    return data

def make_sent_dict(fp):
    scores = {} # initialize an empty dictionary
    for line in fp:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        term = u'term'
        scores[term] = int(score)  # Convert the score to an integer.
#    print scores.items() # Print every (term, score) pair in the dictionary
    return scores


def get_sentiment(line, this_sentiment):
    sent_total = 0

    #
    # Make sure everything is unicode
    #
    for word in line.split():
        word = re.sub(ur'[^a-zA-Z]+', u'', word, flags=re.UNICODE)
        #word = re.sub(ur'[^a-zA-Z]+', u'', word)      
        word = word.lower()

        if word in this_sentiment.keys():
            sent_total += this_sentiment[word]
        else:
            next
# Return total sentiment value 
    return sent_total
               

def lines(fp):
    return str(len(fp.readlines()))
  
def main():

#    sys.stdout = codecs.getwriter('utf-8')(sys.stdout) 
    sent_file  = open(sys.argv[1])
    tweet_file =  open(sys.argv[2])
    if len(sys.argv) ==3:
        DEBUG = "TRUE"
    else:
        DEBUG = NULL

    
    all_tweets = parse_tweets(tweet_file)
    state_sents = {}
    num_deleted = 0
    num_active = 0
    num_words = 0

    sentiments = make_sent_dict(sent_file)
#    print "length of sentiments is %d" % len(sentiments)
    # Parse all tweets
    for i in range(1,len(all_tweets)):
        #
        # Only work with tweets with valid "place" fields (e.g. Fresno, CA, Chile)
        #
        if all_tweets[i]['place']:
            location = all_tweets[i]['place']['full_name']
       
            #
            # "this location = %s" % location
            this_state = location.split(",")        
            if len(this_state) > 1:
                state = this_state[1]
                state = re.sub(ur'[\s]+',u'',state)
                    
                if state in states:
                    country = "US"
                    #print "\tstate = %s  country = %s" % (state, country)
                    #print "\tfound US state for %s" % state
                    line =  all_tweets[i]['text']
                    state_sentiment = get_sentiment(line, sentiments)
                    #print "\tstate sentiment = %d" % state_sentiment
                    if state in state_sents.keys():
                        state_sents[state] += state_sentiment
                    else:
                        state_sents[state]  = state_sentiment

                else:
                    #print "\tNo US state found for %s" % state
                    next
            else:
                    #print "\tOnly country found: %s" % this_state[0]
                    next
        else:
            #print "error: location %s" % all_tweets[i]['place']
            next
    
    sorted_s = sorted(state_sents.iteritems(), key=operator.itemgetter(1))
    print "%s" % sorted_s[len(sorted_s)-1][0]
    

if __name__ == '__main__':
    main()
