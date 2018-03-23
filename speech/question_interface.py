from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Student, Class, Topic, Question, Completion, Keyword, RawText, KeywordContext, Teacher, QuestionImage
from .data import updateSingleTopicProgress, getPercentString, greatestCompletionByStudent, getClassesOfStudent

from nltk.stem import WordNetLemmatizer

import re

class Counter:
    def __init__(self):
        self.fast_counter = 0
        self.slow_counter = 0

    def increment(self):
        self.fast_counter += 1
        if self.fast_counter % 2 == 0:
            self.slow_counter += 1

        return ""


def class_page(request):

    if (request.user.groups.filter(name='student').exists()):
        studentObj = Student.objects.get(user_id_login=request.user.id)
        classes = getClassesOfStudent(studentObj.student_id)
        return render(request, 'class.html', {'classes': classes})
    
    elif (request.user.groups.filter(name='teacher').exists()):
        return HttpResponseRedirect('/teacher')

    else:
        return HttpResponseRedirect('/')


def topic_page(request, class_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    topics = Topic.objects.all().filter(class_id=class_id)
    class_ = Class.objects.get(class_id=class_id)

    # foreach loop to add a field to each topic, giving the percent
    for topic in topics:
        topic.progress = getPercentString(topic.topic_id, request.user.id)

    context = {'class': class_,
               'topics': topics
               }

    return render(request, 'topics.html', context)


def question_page(request, class_id, topic_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')
    studentObj = Student.objects.get(user_id_login=request.user.id)
    class_ = Class.objects.get(class_id=class_id)
    topic = Topic.objects.filter(class_id=class_id).filter(topic_id=topic_id).get()
    questions = Question.objects.filter(class_id=class_id).filter(topic_id=topic_id)

    # foreach loop to add student's highest score to each question
    for question in questions:
        question.best = greatestCompletionByStudent(question.question_id, studentObj.student_id)
        question.percent_to_pass = int(question.percent_to_pass * 100)

    context = {'questions': questions,
               'class': class_,
               'topic': topic,
               }
    return render(request, 'questions.html', context)


def speech(request, class_id, topic_id, question_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    q = Question.objects.get(class_id=class_id, topic_id=topic_id, question_id=question_id)

    if request.method == 'POST':
        context = correct(request, class_id, topic_id, question_id)
        return render(request, 'review.html', context)

    else:
        topic = q.topic_id.topic_name
        topic_id = q.topic_id
        class_ = q.class_id
        images = QuestionImage.objects.filter(question_id = q)

        context = {'q': q,
                   'topic': topic,
                   'class': class_,
                   'topic_id': topic_id,
                   'images': images
                   }

        return render(request, 'speech.html', context)


def correct(request, classId, topicId, questionId):
    lemmatizer = WordNetLemmatizer()
    studentObj = Student.objects.get(user_id_login=request.user.id)
    questionObj = Question.objects.get(class_id=classId, topic_id=topicId, question_id=questionId)

    keywords = Keyword.objects.filter(question_id=questionId, is_primary=True)
    studentResponse = request.POST['final_transcript']
    keywordDict = {}

    studentScore = 0
    possibleScore = 0

    # add words to dictionary with point values
    for keywordObj in keywords:
        word = keywordObj.keyword.lower()
        hint = keywordObj.hint
        possibleScore += keywordObj.point_value
        if keywordDict.get(word) == None:
            keywordDict[word] = { 'points': keywordObj.point_value, 'hint': keywordObj.hint }

    # studentResponse = re.sub("~!@#$%^&*()_+=-`/*.,[];:'/?><", ' ', studentResponse)
    #replace illegal characters with a space

    # add student score

    kw_list = []
    prev_context_list = []
    post_context_list = []
    other_words = []

    nonkw = ""

    studentResponseLemmatized = [lemmatizer.lemmatize(re.sub(r'\W+', '', item.lower())) for item in studentResponse.split()]

    studentResponseList = studentResponse.split(' ')

    for idx, word in enumerate(studentResponseLemmatized):
        if keywordDict.get(word) is not None:
            studentScore += keywordDict[word]['points']
            keywordDict[word]['points'] = 0 # set the point value to 0 bc the points have already been earned

            # Add the NON Lemmatized word for output
            kw_list.append(studentResponseList[idx])

            kw = Keyword.objects.get(question_id=questionObj, keyword=word, is_primary=True)

            contextObj = KeywordContext.objects.get(question_id=questionObj, keyword=kw, previous=True)
            prev_context_list.append(contextObj)

            contextObj = KeywordContext.objects.get(question_id=questionObj, keyword=kw, previous=False)
            post_context_list.append(contextObj)

            other_words.append(nonkw)
            nonkw = ""
        else:
            nonkw = nonkw + studentResponseList[idx] + " "

    other_words.append(nonkw)
    kw_list.append("")

    # Find the lowest valued missed word to recommend
    recommended_keyword = ''
    recommended_keyword_value = 0

    for idx, pair in enumerate(keywordDict):
        numPoints = float(keywordDict[pair]['points'])
        word = keywordDict[pair]['hint']
        if (recommended_keyword is '' or (numPoints > 0 and numPoints < recommended_keyword_value)):
            recommended_keyword = word
            recommended_keyword_value = numPoints

    interleaved_transcript = []
    i = 0
    while i < len(other_words):
        interleaved_transcript.append(other_words[i])
        interleaved_transcript.append(kw_list[i])
        i += 1

    counter_instance = Counter()

    # create completion object
    completion = Completion.objects.create(student_id=studentObj,
                                           question_id=questionObj,
                                           transcript=studentResponse,
                                           percent_scored=float(studentScore) / possibleScore)

    # create or update topic progress
    updateSingleTopicProgress(request.user.id, topicId)

    # did the student pass?
    if float(studentScore) / possibleScore > questionObj.percent_to_pass:
        resultString = "Pass"
    else:
        resultString = "Fail"

    # give the front end neccesary context
    context = {
        'q': questionObj,
        'percentage': str(int(1000 * studentScore / possibleScore) / 10),
        'name': studentObj.f_name,
        'transcript': interleaved_transcript,
        'prev_context_list': prev_context_list,
        'post_context_list': post_context_list,
        'counter': counter_instance,
        'result_string': resultString,
        'percent_to_pass': str(100 * questionObj.percent_to_pass),
        'perfect_answer': questionObj.perfect_answer,
        'recommended_keyword': recommended_keyword
    }

    return context