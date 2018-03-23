from .models import Student, Topic, Question, Completion, TopicProgress, Class, Enrollments
from django.db.models import Max

def updateProgressesFromTopic(topicId):

	topicProgressQuery = TopicProgress.objects.filter(topic_id = topicId)
	numberOfQuestions = numQuestionsInTopic(topicId)
	topicProgressQuery.update( total_questions = numberOfQuestions )


def updateSingleTopicProgress(userId, topicId):

    studentObj = Student.objects.get(user_id_login = userId)

    topicProgress = TopicProgress.objects.filter(student_id = studentObj.student_id, topic_id = topicId)

    questionCount = numQuestionsInTopic(topicId)
    answeredCount = numQuestionsAnsweredByStudent(topicId, studentObj.student_id)

    if topicProgress.count() > 0: #topicProgress exists

        topicProgress.update(   num_answered = answeredCount,
                                total_questions = questionCount )

    else: #topicProgress does not exist
        
        topicObj = Topic.objects.get(pk=topicId)
        classObj = Class.objects.get(pk=topicObj.class_id.class_id)

        TopicProgress.objects.create(   student_id = studentObj,
                                        topic_id = topicObj,
                                        class_id = classObj,
                                        num_answered = answeredCount,
                                        total_questions = questionCount    )

def getPercentString(topicId, userId):

    studentObj = Student.objects.get(user_id_login = userId)
    topicProgress = TopicProgress.objects.filter(student_id = studentObj.student_id, topic_id = topicId)
    questionCount = numQuestionsInTopic(topicId)
    answeredCount = numQuestionsAnsweredByStudent(topicId, studentObj.student_id)

    if topicProgress.count() > 0: #topicProgress exists

        return (answeredCount * 100 / questionCount)

    else: #topicProgress does not exist

        return 0


def getTopicProgressesForStudent(classId, userId):

    studentObj = Student.objects.get(user_id_login = userId)
    studentId = studentObj.student_id

    return TopicProgress.objects.filter()


def numQuestionsInTopic(topicId):
    
    queryResult = Question.objects.filter(topic_id = topicId)
    return queryResult.count()


def numQuestionsAnsweredByStudent(topicId, studentId):

    questionsInTopic = Question.objects.filter(topic_id = topicId)
    count = 0
    for index, question in enumerate(questionsInTopic):
        questionResponses = Completion.objects.filter(question_id = question.question_id, student_id = studentId, percent_scored__gte = question.percent_to_pass)
        if questionResponses.count() > 0:
            count += 1
    return count

def greatestCompletionByStudent(questionId, studentId):

    allCompletions = Completion.objects.filter(question_id = questionId, student_id = studentId)
    if (allCompletions.count() > 0):
        bestCompletion = allCompletions.order_by("-percent_scored")[0]
        return int(bestCompletion.percent_scored * 100)
    else:
        return 0

def getClassesOfStudent(studentId):

    enrollments = Enrollments.objects.filter(student_id = studentId)
    searchArray = []
    for e in enrollments:
        searchArray.append(e.class_id.class_id)
    return Class.objects.filter(class_id__in=searchArray)

def getStudentBestScore(request, questionId):

    if request.method == 'GET':

        studentObj = Student.objects.get(user_id_login = userId)
        studentId = studentObj.student_id

        bestCompletion = Completion.objects.get(student_id = studentId, question_id = questionId)
        response = serializers.serialize("json", [bestCompletion])
        return HttpResponse(json.dumps(response), content_type='application/json')