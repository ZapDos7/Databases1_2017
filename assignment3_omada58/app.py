# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys
import urllib
import re
#from madis import textwindow

def connection():
    ''' User this function to create your connections '''
    import sys
    sys.path.append(settings.MADIS_PATH)
    import madis

    con = madis.functions.Connection('yelp.db')
    
    return con



def classify_review(reviewid):
    
    # Create a new connection
    # Create a new connection

    con=connection()
    cur=con.cursor()

#arxikopohsh var gia na kalesoume textwindow

    cur.execute("select var('id',?)",(reviewid,))


#dhmiourgoume arxeio me ta posterms ths db
    with open("posWords.txt", "w") as file:
        for word in cur.execute("select word from posterms"):
            newRow = str(word)
            start = "(u\'"
            end = "',"
            s = newRow
            s = ((s.split(start))[1].split(end)[0])
            file.write(str(s))
            file.write(str('\n')) 

    file.close()

#dhmiourgoume arxeio me ta negterms ths db
    with open("negWords.txt", "w") as file:
        for word in cur.execute("select word from negterms"):
            newRow = str(word)
            start = "(u\'"
            end = "',"
            s = newRow
            s = ((s.split(start))[1].split(end)[0])
            file.write(str(s))
            file.write(str('\n')) 

    file.close()

#arxikopoihsh metritwn
    negCount = 0
    posCount = 0
    wordsFound = []      
    for cu in cur.execute("select textwindow(text,0,0) from reviews where review_id = var('id')"):
        row = str(cu)

        s = row

#elegxos thetikwn le3ewn pou vrethikan sto keimeno
        with open("posWords.txt", "r") as file:
            for word in file:              
                end = "\n"
                word = word.split(end)[0]
                # elegxos memonomena ths le3hs frashs    
                if re.search(r'\b' + word +r'\b', s):

                    wordsFound.append(word)
                    posCount+=1

                    for x in word:
                        if x == ' ':
                            posCount+=1

#epipleon pra3eis gia ton teliko upologismo 
#trexoume epalanipsh mesa sthn lista me tis le3eis pou vrhkame
#prokeimenou na diorthosoume ton counter opou xreiazetai

    for x in wordsFound:
        for y in wordsFound:
            if (x in y and len(x) < len(y)):
                print x
                print "einai substring"
                print y
                posCount-=1
                for z in x:
                    if z == ' ':
                        posCount-=1                             

    print wordsFound
    print posCount

    wordsFound = []

#### EPANALAMVANETAI H DIADIKASIA ANTISTOIXWS GIA TA NEGTERMS ####
    for cu in cur.execute("select textwindow(text,0,0) from reviews where review_id = var('id')"):
        row = str(cu)

        s = row

        with open("negWords.txt", "r") as file:
            for word in file:              
                end = "\n"
                word = word.split(end)[0]

                if re.search(r'\b' + word +r'\b', s):

                    wordsFound.append(word)
                    negCount+=1

                    for x in word:
                        if x == ' ':
                            negCount+=1


    for x in wordsFound:
        for y in wordsFound:
            if (x in y and len(x) < len(y)):
                print x
                print "einai substring"
                print y
                negCount-=1
                for z in x:
                    if z == ' ':
                        negCount-=1                       


    file.close()
    print wordsFound
    print negCount
#upologismos an ta review einai thetika h arnhtika
# <0 arnhtiko || >0 thetiko
    posCount = posCount - negCount
    result = []
    result.append(posCount)


#vriskoume to onoma ths etereias
    for row in (cur.execute("select business.name from business,reviews where business.business_id = reviews.business_id and review_id = (?) ",(reviewid,))):
        name = str(row)
    print name

#spame to string prokeimenou na fenetai pio omorfo
    str1 = name.replace("(u'", "")
    str2 = str1.replace("',)", "")
    name = str2
    str1 = name.replace('(u"', '')
    str2 = str1.replace('",)', "")
    name = str2
    print name
    bName = []
    bName.append(str(name))

#epistrefei apotelesmata
    return [("business_name","result"), (bName,result)]


def classify_review_plain_sql(reviewid):

    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    cur1 = con.cursor()

    count = 1

#H DIADIKASIA EPANALAMVANETAI KAI EDW OPWS E3HGHSAME PROIGOUMENOS STHN
#PANW SUNARTHSH || KYRIA DIAFORA EINAI OTI EDW ELEGXOUME KAI FRASEIS EKTOS APO LE3EIS
    with open("posWords.txt", "w") as file:
        for word in cur.execute("select word from posterms"):
            newRow = str(word)
            start = "(u\'"
            end = "',"
            s = newRow
            s = ((s.split(start))[1].split(end)[0])
            file.write(str(s))
            file.write(str('\n'))
 
    file.close()

    with open("negWords.txt", "w") as file:
        for word in cur.execute("select word from negterms"):
            newRow = str(word)
            start = "(u\'"
            end = "',"
            s = newRow
            s = ((s.split(start))[1].split(end)[0])
            file.write(str(s))
            file.write(str('\n'))
 
    file.close()

    with open("output.txt", "w") as text_file:
        for row in cur.execute("select text from reviews where review_id = (?)",(reviewid,)):

            text_file.write(str(row))
            text_file.write(' ')
            text_file.write('\n')


    text_file.close()    

    with open("output.txt", "r") as text_file:
        review = text_file.read().replace('\n','')

    text_file.close()

    with open("posWords.txt", "r") as text_file:

        wordsFound=[]
        posCount = 0

        for word in text_file:
            end = "\n"
            word = word.split(end)[0]
   
            if re.search(r'\b' + word +r'\b', review):

                wordsFound.append(word)
                posCount+=1

                for x in word:
                    if x == ' ':
                        posCount+=1
 

    y = len(wordsFound)
    for x in wordsFound:
        for y in wordsFound:
            if (x in y and len(x) < len(y)):
                print x
                print "einai substring"
                print y
                posCount-=1
                for z in x:
                    if z == ' ':
                        posCount-=1                 

    text_file.close()                



    print posCount

    print wordsFound

    with open("negWords.txt", "r") as text_file:

        wordsFound=[]
        negCount = 0

        for word in text_file:
            end = "\n"
            word = word.split(end)[0]
   
            if re.search(r'\b' + word +r'\b', review):

                wordsFound.append(word)
                negCount+=1

                for x in word:
                    if x == ' ':
                        negCount+=1



    text_file.close()

    y = len(wordsFound)
    for x in wordsFound:
        for y in wordsFound:
            if (x in y and len(x) < len(y)):
                print x
                print "einai substring"
                print y
                negCount-=1
                for z in x:
                    if z == ' ':
                        negCount-=1



#WATCH SXOLIA STHN PROIGOUMENH SUNARTHSH
    print wordsFound
    print negCount
    posCount = posCount - negCount
    result = []
    result.append(posCount)

    for row in (cur.execute("select business.name from business,reviews where business.business_id = reviews.business_id and review_id = (?) ",(reviewid,))):
        name = str(row)

    str1 = name.replace("(u'", "")
    str2 = str1.replace("',)", "")
    name = str2
    str1 = name.replace('(u"', '')
    str2 = str1.replace('",)', "")
    name = str2
    print name
    bName = []
    bName.append(str(name))

    return [("business_name","result"), (bName,result)]

def updatezipcode(business_id,zipcode):
    
   # Create a new connection
    
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    print business_id, " result ", zipcode
    new_zipcode = 1000000

    for row in cur.execute("select distinct zip_code from business where business_id = (?) ", (business_id,)):
       new_zipcode = str(row)

    if new_zipcode != 1000000 and (zipcode.isdigit() and (len(zipcode) == 5)):
        print "ok, zipcode changed to " , zipcode
        apotelesma = "ok"
        cur.execute("update business set zip_code = (?) where business_id = (?)", (zipcode,business_id,))
    else:
        print "error"
        apotelesma = "error"    

    
    return [("result",apotelesma,),]
    
    
def selectTopNbusinesses(category_id,n):
    #CATEGORY_ID (1..727)
    # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    cur1 = con.cursor()    
    n = int(n)

    allb_ids = []
    
    for row in cur.execute("select business_id from business_category where category_id = (?)", (category_id,)): #gi auto to cat_id
        b_id = str(row) #exw auta ta b_id
        
        string1 = b_id
        str1 = string1.replace("(u'", "")
        str2 = str1.replace("',)", "")
        b_id = str2
        allb_ids.append(b_id)

    #print 'All business IDs are ' + str(allb_ids)
    k = len(allb_ids) #posa IDs exei h kathgoria auth
    
    pairs = []

    for x in range(0,k):
        posrev = 0
        tempb_id = allb_ids[x]
        for row in cur.execute("select reviews.review_id from reviews, reviews_pos_neg where positive = 1 and business_id = (?) and reviews.review_id = reviews_pos_neg.review_id ", (tempb_id,)):
            posrev += 1 #epistrefei posa positive reviews exei auto to b_id


        pairs.append((tempb_id,posrev))

        sort_pairs = sorted(pairs, key = lambda kati: kati[1])

    final_pairs = []
    for i in reversed(sort_pairs):
        final_pairs.append(i)

    business_id1 = []
    numberOfreviews1 = []

    if k < n:
        print 'You asked for more than we can give :('
        n = k

    for y in range (0,n):
        business_id1.append(final_pairs[y][0]) # to ka8e b_id gia n epi8umhta results 

    for q in range (0,n):    
        numberOfreviews1.append(final_pairs[q][1]) #antistoixa num of reviews

    return [("business_id", "numberOfreviews"),(business_id1, numberOfreviews1),]

def traceUserInfuence(userId,depth):
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    


    return [("user_id",),]






# coding: utf-8