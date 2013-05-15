import sys
import json
import string
import re

def make_sent_dict(fp):
    scores = {} # initialize an empty dictionary
    for line in fp:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
#    print scores.items() # Print every (term, score) pair in the dictionary
    return scores

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


def lines(fp):
    return str(len(fp.readlines()))
  
def main():
    sent_file  = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiments = make_sent_dict(sent_file)
    
    all_tweets = parse_tweets(tweet_file)
    for i in range(0,len(all_tweets)):
     #   print all_tweets[i]['lang'] 
#        if all_tweets[i]['lang'] == "en":

        try:
            line =  all_tweets[i]['text']
            sentiment_score = 0    
            for word in line.split():
                #
                # Clean up the words (remove hashtags, URLS, punctuation, etc. )
                #
#                if re.search(r"(^[#@]+)", word):
#                     next


                if word in sentiments.keys():
                    #print word, sentiments[word]
                    sentiment_score += sentiments[word]
                else:
                    next
                    #print word, "0"
            print '%d' % (sentiment_score)
        except:    
            next
        
if __name__ == '__main__':
    main()
