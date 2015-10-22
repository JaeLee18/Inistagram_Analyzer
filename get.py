from instagram.client import InstagramAPI
import urllib2
import urllib
import json

#Constants to check the number of Post.
positive = 0
negative = 0
netural = 0

#Keys for Instagram API
access_token = "1997307189.6b69e77.ef755b6606bf4e7e9b1c452587eaaaba"
client_secret = "c760225bb9cf43c89105a63f746846a5"
api = InstagramAPI(access_token=access_token, client_secret=client_secret)

#Get recent 20 posts which have #CapitalOne
url = 'https://api.instagram.com/v1/tags/CapitalOne/media/recent?access_token=1997307189.1fb234f.53a2d32698954f1087d3a1f23449c2ed'

#Load the result.
json_file = urllib2.urlopen(url)
json_data = json.load(json_file)

#Make an array which contains 20 of posts.
text = [ ]
for i in range(20):
    text.append(json_data["data"][i]["caption"]["text"])
    

#Filter Emojis in each Post and Determine whether a post contains positive, negative or netural
#toward to Capital one
    
no_emoji = [ ] #no_emoji -> An array which is exactly same as 'text' array but it does not have any emojis.
response = [ ] #response -> An array which stores sentiments of posts.
for i in range(20):
    no_emoji.append(text[i].encode('ascii', 'ignore').decode('ascii'))
    text_encode = urllib.urlencode({"text": no_emoji[i]}) 
    text_data = urllib2.urlopen("http://text-processing.com/api/sentiment/", text_encode)
    text_json_data = json.load(text_data)
    response.append(text_json_data["label"])
    if (response[i] == "pos"):
        positive += 1
    elif (response[i] == "neg"):
       negative += 1
    else:
        netural += 1

# Calculate Percentages of Positive, Negative and Netural Posts.
percent_positive = str(((float)(positive)/float(20))*100) + "%"
percent_negative = str(((float)(negative)/float(20))*100) + "%"
percent_netural = str(((float)(netural)/float(20))*100) + "%"

# Count Number of Likes
likes = [ ] #like -> An array which stores the number of like from each post.
for i in range(20):
    likes.append(json_data["data"][i]["likes"]["count"])

    

#--------------------------------------------------Get User Information------------------------------------------------------------------------------------------------------------------------------------#
#Get User Id
user_id = [ ]
for i in range(20):
    user_id.append(json_data["data"][i]["user"]["id"]);

#Get Each User's Url to get their infomation.    
url_user_id = [ ]
for i in range(20):
    url_user_id.append('https://api.instagram.com/v1/users/' + str(user_id[i]) + "?access_token=1997307189.1fb234f.53a2d32698954f1087d3a1f23449c2ed")
    

#Get Each User's information and Open Each User's Url
user_id_json_file = [ ]
for i in range(20):
    user_id_json_file.append(urllib2.urlopen(url_user_id[i]))

#Get Users' Information in JSON Format
user_id_json_data = [ ]
for i in range(20):
    user_id_json_data.append(json.load(user_id_json_file[i]))

# Get Number of Users posts
numOfMedia = [ ]
for i in range(20):
    numOfMedia.append(user_id_json_data[i]["data"]["counts"]["media"])
    
#Get Number of Users Followers
numOfFollowers = [ ]
for i in range(20):
    numOfFollowers.append(user_id_json_data[i]["data"]["counts"]["follows"])

#Get Number of People who follow this user
numOfFollowed = [ ]
for i in range(20):
    numOfFollowed.append(user_id_json_data[i]["data"]["counts"]["followed_by"])

#----------------------------------------------------------------------------------Summary-----------------------------------------------------------------------------------------------------------------#
    
for i in range(20):
    print "Post #" + str(i + 1) +": " + text[i]
    print "Number of Likes for This Post Is:  " + str(likes[i])
    print "This User" + "(user_id: " + user_id[i] + ")" + " has " + str(numOfMedia[i]) + " posts."
    print "Also, this user has "+ str(numOfFollowers[i]) + " followers."
    print "And " + str(numOfFollowed[i]) + " people follow this user.\n"




print "\n#--------------------------Recent 20 Posts with #CapitalOne Anaylsis Summary------------------------------------#"
print "      - Number of Positive Posts: " + str(positive) 
print "      - Number of Negative Posts: " + str(negative)
print "      - Number of Netural Posts:  " + str(netural) + "\n"
print "      - Percentage of Positive Posts in 20 Posts: " + percent_positive
print "      - Percentage of Negative Posts in 20 Posts: " + percent_negative
print "      - Percentage of Netural Posts in 20 Posts:  " + percent_netural
print "#---------------------------------------------------------------------------------------------------------------#"
