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
    tweet_file =  open(sys.argv[1])
    if len(sys.argv) == 1:
        DEBUG = "TRUE"
        print "DEBUG Mode ON"

    
    all_tweets = parse_tweets(tweet_file)
    hash_dict = {}
    num_deleted = 0
    num_active = 0
    num_words = 0

    # Parse all tweets
    for i in range(1,len(all_tweets)):
        #
        # Only work with tweets with valid "hashtags" fields 
        #
        if all_tweets[i]['entities']['hashtags']:
            h =  all_tweets[i]['entities']['hashtags']
            if len(h) > 0:
                for i in range(0,len(h)):
                    hashtag = h[i]['text']
                    if hashtag in hash_dict.keys():
                        hash_dict[hashtag] += 1
                    else:
                        hash_dict[hashtag]  = 1
            else:
                next
        else:
            next
    
    sorted_h = sorted(hash_dict.iteritems(), key=operator.itemgetter(1))
    min = len(sorted_h)-11
    max = len(sorted_h)-1
    #print "min max %d %d" % (min, max)
    #for i in range(len(sorted_h)-1, len(sorted_h)-11):
    for i in range(max,min,-1 ):
        
        print "%s %f" % (sorted_h[i][0], hash_dict[sorted_h[i][0]] )
    

if __name__ == '__main__':
    main()
