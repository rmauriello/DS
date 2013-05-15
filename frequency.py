import sys
import json
import string
import re
    

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
    tweet_file = open(sys.argv[1])

    
    all_tweets = parse_tweets(tweet_file)
    tfm = {}
    num_deleted = 0
    num_active = 0
    num_words = 0
    # Parse all tweets
    for i in range(1,len(all_tweets)):
        if 'delete' in all_tweets[i].keys():
            num_deleted += 1
            next
        else:
            num_active += 1

        try:
            line =  all_tweets[i]['text']
              
            for word in line.split():
                #
                # Clean up the words (remove hashtags, URLS, punctuation, etc. )
                #
                #print "word %s" % word                 
                word = re.sub(ur'[^a-zA-Z]+', u'', word, flags=re.UNICODE)
#                word = word.lower()
#                if word.isspace():
#                    print "skipping blank word"
#                    next

                num_words += 1

                if word in tfm.keys():
                    tfm[word] += 1
                    #print "Incrementing word %s : %d" % word, tfm[word]
                else:
                    tfm[word] = 1
                                            #print "Adding word to dict %s" % word
        except:  
            #print e  
            next

#    print "number of active tweets %d" % num_active
#    print "number of deleted tweets %d" %num_deleted
#    print "length of tfm is %d" % len(tfm)
#    print "total number of words %d" % num_words


#    num_words = 0
#    for key in sorted(tfm.iterkeys()):
#        num_words = num_words + tfm[key]
#    print "total words = %d" % num_words

    for key in sorted(tfm.iterkeys()):
        print "%s %f" % (key, float(tfm[key])/num_words)
    
        
if __name__ == '__main__':
    main()
