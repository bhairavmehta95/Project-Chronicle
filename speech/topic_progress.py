from .models import Student, Topic, Question, Completion, TopicProgress, Class

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
        classObj = Class.objects.get(pk=topicObj.class_id)

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

        print ("answered: " + str(answeredCount))
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
    for question in questionsInTopic:
        questionResponses = Completion.objects.filter(question_id = question.question_id, student_id = studentId)
        if questionResponses.count() > 0:
            count += 1
    return count