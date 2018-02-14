from steem import Steem
import pandas as pd

node = ["https://api.steemit.com"]
s = Steem(node)

# start: '2018-02-11T10:56:33'
# end: '2018-02-13T16:03:42'
# normal limit = 10000


names = []
timestamp = []
self_upvotes = []
upvotes = []
amount = []
price = []
downvotes = []
len_upvote_receiver = []

x = 0

#http://www.steemdollar.com/vests.php: Vests/x = Steem

def vests_to_sp(vests):
    #update mvests value before use!
    mvests = 2044.5983714162855

    return vests / mvests

def get_upvote_stats(user):

    votes = s.get_account_votes(user)

    self_upvotes = 0
    upvotes = 0
    downvotes = 0
    upvote_receiver = []

    for i in votes:
        if (i["time"]>="2018-02-12T14:50:12"):

            author = i["authorperm"].split("/")[0]

            #downvotes
            if(int(i["percent"])<0):
                downvotes += 1

            #self upvotes
            if (author==user):
                self_upvotes += 1

                if not author in upvote_receiver:
                    upvote_receiver.append(author)

            #normal upvotes
            else:
                if (i["percent"]>0):
                    upvotes += 1

                if not author in upvote_receiver:
                    upvote_receiver.append(author)

    return self_upvotes,upvotes,len(upvote_receiver),downvotes


history = s.get_account_history('blocktrades', index_from=1350000, limit=10000)

for i in history:
    if (i[1]["op"][0]=="delegate_vesting_shares"):

        timestamp.append(i[1]["timestamp"])
        names.append(i[1]["op"][1]["delegatee"])

        SP = vests_to_sp(float(i[1]["op"][1]["vesting_shares"].split(" ")[0]))

        if (SP != None):

            amount.append(str(SP).replace(".",","))

            pricecal = (float(amount[x].replace(",",".")) / 1841.635) * 885.15
            price.append(str(pricecal).replace(".",","))

        # 1 ETH --> 1841.635 SP
        # 1 ETH --> 885.15$

        else:
            price.append("?")

        x += 1


for i in names:

    data = get_upvote_stats(i)

    self_upvotes.append(data[0])
    upvotes.append(data[1])
    len_upvote_receiver.append(data[2])
    downvotes.append(data[3])



d = {"names":names, "timestamp": timestamp, "self upvotes":self_upvotes, "upvotes": upvotes, "amount of SP":amount, "price in $": price, "different upvote receiver": len_upvote_receiver, "downvotes":downvotes}
df = pd.DataFrame(data=d)

df.to_csv("delegations2.csv",sep=",")

print(df)
