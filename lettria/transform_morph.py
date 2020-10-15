def addLem(lem, lemToAdd):
    if lemToAdd :
        if lem == '_':
            return lemToAdd
        else :
            return lem + '|' + lemToAdd


def transform_data(data):
    res = []
    if not isinstance(data, list):
        data = [data]
    for d in data:
        lem = '_'
        w = []
        w.append(d['source'])
        if 'lemmatizer' not in d.keys():
            w.append(d['source'])
        elif type(d["lemmatizer"]) is dict:
            if "infinit" in d["lemmatizer"].keys():
                w.append(d['lemmatizer']['infinit'])

            elif "lemma" in d["lemmatizer"].keys():
                if d['lemmatizer']["lemma"] != "":
                    w.append(d['lemmatizer']['lemma'])
                else:
                    w.append(d['source'])

            else:
                w.append(d['source'])

            lemmatizer = d['lemmatizer']


        elif type(d['lemmatizer']) is list:
            if 'infinit' in d['lemmatizer'][0].keys():
                w.append(d['lemmatizer'][0]['infinit'])

            elif 'infinit' in d['lemmatizer'][1].keys():
                w.append(d['lemmatizer'][1]['infinit'])

            else:
                w.append(d['source'])

            lemmatizer = d['lemmatizer'][0]


        else:
            w.append(d['source'])

        if 'gender' in lemmatizer.keys() :
            try:
                if lemmatizer['gender']['female']==True:
                    gender = 'Gender=Fem'
                elif lemmatizer['gender']['female']==False:
                    gender = 'Gender=Masc'
                lem = addLem(lem, gender)
            except:
                pass
                # print("Update 20191105 - CCO add exception : No female is present in key gender for word '{}'. Key = {}".format(d["source"], lemmatizer))

            try:
                if lemmatizer['gender']['plural']==True:
                    number = 'Number=Plur'
                elif lemmatizer['gender']['plural']==False:
                    number = 'Number=Sing'
                lem = addLem(lem, number)
            except:
                pass
                # print("Update 20191105 - CCO add exception : No plural is present in key gender for word '{}'. Key = {}".format(d["source"], lemmatizer))

            #Disjunct cases, not yes exhaustive. Should it be ?? Check in code how it is treated.
        if 'conjugate' in lemmatizer.keys() :
            if len(lemmatizer['conjugate']) == 1:
                try:
                    mode = lemmatizer['conjugate'][0]['mode']
                    if mode == 'indicative':
                        mood = 'Mood=Ind'
                    elif mode == 'subjonctive':
                        mood = 'Mood=Sub'
                    elif mode == 'conditional':
                        mood = 'Mood=Cnd'
                    elif mode == 'imperative':
                        mood = 'Mood=Imp'
                    elif mode == 'infinitive':
                        mood = 'VerbForm=Inf'
                    lem = addLem(lem, mood)
                except:
                    pass
                    # print("Update 20191105 - CCO add exception : No mood is present in key conjugate for word '{}'. Key = {}".format(d["source"], lemmatizer['conjugate']))
                try:
                    person = "Person=" + str(lemmatizer['conjugate'][0]['pronom'])
                    lem = addLem(lem, person)
                except:
                    pass
                    # print("Update 20191105 - CCO add exception : No person is present in key conjugate for word '{}'. Key = {}".format(d["source"], lemmatizer['conjugate']))

                try:
                    if int(lemmatizer['conjugate'][0]['pronom']) in [1, 2, 3]:
                        number = "Number=Sing"
                    elif int(lemmatizer['conjugate'][0]['pronom']) in [4, 5, 6]:
                        number = "Number=Plur"
                    lem = addLem(lem, number)
                except:
                    pass
                    # print("Update 20191105 - CCO add exception : No number is present in key conjugate for word '{}'. Key = {}".format(d["source"], lemmatizer['conjugate']))


                # Analogically with conjugate, we might be supposed to disjunct cases

                try:
                    temps = str(lemmatizer['conjugate'][0]['temps'])
                    if temps == 'present':
                        tense = "Tense=Pres"
                    elif temps == '':
                        tense = "Tense=Imp"
                    elif temps == 'past':
                        tense = "Tense=Past"
                    elif temps == 'future':
                        tense = "Tense=Fut"
                    lem = addLem(lem, tense)
                except:
                    pass
                    # print("Update 20191105 - CCO add exception : No tense is present in key conjugate for word '{}'. Key = {}".format(d["source"], lemmatizer['conjugate']))

                try:
                    if mood:
                        verbform = "VerbForm=Fin"
                        lem = addLem(lem, verbform)
                except:
                    pass
                    # print("Update 20191105 - CCO add exception : No mood is present in key conjugate for word '{}'. Key = {}".format(d["source"], lemmatizer['conjugate']))



        if 'mode' in lemmatizer.keys() :
            mode = lemmatizer['mode']
            try:
                if mode == 'define':
                    definite = 'Definite=Def'
                    lem = addLem(lem, definite)
                elif mode == 'undefine':
                    definite = 'Definite=Ind'
                    lem = addLem(lem, definite)
            except:
                pass
                # print("Update 20191105 - CCO add exception : No definite is present in key mode for word '{}'. Key = {}".format(d["source"], lemmatizer))


        elif 'lemma' in lemmatizer.keys():
            if lemmatizer['lemma'] in ['un', 'une']:
                definite = 'Definite=Ind'
                try:
                    lem = addLem(lem, definite)
                except:
                    pass
                    # print("Update 20191105 - CCO add exception : No definite is present in key definite for word '{}'. Key = {}".format(d["source"], lemmatizer))


        if 'tag' in d.keys():
            tag = d['tag']
            if tag=='D' or tag=='PD' :
                if 'mode' in lemmatizer.keys():
                    if lemmatizer['mode'] == 'demonstrative':
                        prontype = 'PronType=Dem'
                    elif lemmatizer['mode'] == 'possessive':
                        prontype = 'Poss=Yes|PronType=Pos'
                    elif lemmatizer['mode'] == 'define':
                        prontype = 'PronType=Art'
                    elif 'pronom' in lemmatizer.keys():
                        try:
                            person = "Person=" + str(lemmatizer['pronom'])
                            lem = addLem(lem, person)
                        except:
                            pass
                            # print("Update 20191105 - CCO add exception : No person is present in key conjugate for word '{}'. Key = {}".format(d["source"], lemmatizer))

                        try:
                            number = "Number=Sing" if int(lemmatizer['pronom']) <= 3 else "Number=Plur"
                            lem = addLem(lem, number)
                        except:
                            pass
                            # print("Update 20191105 - CCO add exception : No number is present in key conjugate for word '{}'. Key = {}".format(d["source"], lemmatizer))

                        prontype = 'PronType=Prs'
                    try:
                        lem = addLem(lem, prontype)
                    except:
                        pass
                        # print("Update 20191105 - CCO add exception : No prontype is present in key conjugate for word '{}'. Key = {}".format(d["source"], lemmatizer))
                elif 'category' in lemmatizer.keys():
                    if lemmatizer['category'] == 'negation':
                        prontype = 'PronType=Neg'
            if tag == "VP" :
                try:
                    lem = addLem(lem, "VerbForm=Part")
                    lem = addLem(lem, "Tense=Past")
                except:
                    pass
                    # print("Update 20191112 - CCO add exception")

            if tag == "CLO":
                print(lemmatizer)
                if lemmatizer["lemma"] == "se":
                    lem = addLem(lem, "Reflex=Yes")
                    if d["source"] == "se":
                        lem = addLem(lem, "Person=3")
                    if d["source"] == "me":
                        lem = addLem(lem, "Person=1")
                        lem = addLem(lem, "Number=Sing")
                    if d["source"] == "te":
                        lem = addLem(lem, "Person=2")
                        lem = addLem(lem, "Number=Sing")
                    if d["source"] == "nous":
                        lem = addLem(lem, "Person=1")
                        lem = addLem(lem, "Number=Plur")
                    if d["source"] == "vous":
                        lem = addLem(lem, "Person=2")
                        lem = addLem(lem, "Number=Plur")

                if lemmatizer["lemma"] == "le":
                    if d["source"] == "me":
                        lem = addLem(lem, "Person=1")
                        lem = addLem(lem, "Number=Sing")
                    if d["source"] == "le":
                        lem = addLem(lem, "Person=3")
                        lem = addLem(lem, "Number=Sing")
                    if d["source"] == "les":
                        lem = addLem(lem, "Person=3")
                        lem = addLem(lem, "Number=Plur")

                if d["source"] == "y":
                    lem = addLem(lem, "Person=3")

            if tag == "CLS":
                if d["source"] == "je":
                    lem = addLem(lem, "Number=Sing")
                    lem = addLem(lem, "Person=1")
                elif d["source"] == "tu":
                    lem = addLem(lem, "Number=Sing")
                    lem = addLem(lem, "Person=2")
                elif d["source"] == "il":
                    lem = addLem(lem, "Number=Sing")
                    lem = addLem(lem, "Person=3")
                    lem = addLem(lem, "Gender=Masc")
                elif d["source"] == "elle":
                    lem = addLem(lem, "Number=Sing")
                    lem = addLem(lem, "Person=3")
                    lem = addLem(lem, "Gender=Fem")
                elif d["source"] == "on":
                    lem = addLem(lem, "Number=Sing")
                    lem = addLem(lem, "Person=3")
                elif d["source"] == "nous":
                    lem = addLem(lem, "Number=Plur")
                    lem = addLem(lem, "Person=1")
                elif d["source"] == "vous":
                    lem = addLem(lem, "Number=Plur")
                    lem = addLem(lem, "Person=2")
                elif d["source"] == "ils":
                    lem = addLem(lem, "Number=Plur")
                    lem = addLem(lem, "Person=3")
                    lem = addLem(lem, "Gender=Masc")
                elif d["source"] == "elles":
                    lem = addLem(lem, "Number=Plur")
                    lem = addLem(lem, "Person=3")
                    lem = addLem(lem, "Gender=Fem")

        if 'category' in lemmatizer.keys():
            if lemmatizer['category'] == 'negation':
                polarity = 'Polarity=Neg'
                try:
                    lem = addLem(lem, polarity)
                except:
                    pass
                    # print("Update 20191105 - CCO add exception : No polarity is present in key conjugate for word '{}'. Key = {}".format(d["source"], lemmatizer))
        res.append(lem)
    return(res)
