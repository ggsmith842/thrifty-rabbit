#!/usr/bin/env python # 

class RiskQuestion:
    def __init__(self, questionText, weight=1):
        self.questionText = questionText
        self.weight = weight
        self.answers = []

class RiskQuestionAnswer:
    def __init__(self, answerText, score, selected = False):
        self.answerText = answerText
        self.score = score
        self.selected = selected

class RiskQuestionnaire:
    def __init__(self):
        self.questions = []                  

    def loadQuestionnaire(self, riskQuestionsFileName, riskAnswersFileName, type):
        if not (type in ["Tolerance", "Capacity"]):
                raise ValueError('Type must be Tolerance or Capacity.')
        import pandas as pd
        riskQuestions = pd.read_csv(
            riskQuestionsFileName).reset_index()
        riskAnswers = pd.read_csv(
            riskAnswersFileName).reset_index()
        if (type == "Tolerance"):
            toleranceQuestions = riskQuestions[(riskQuestions['QuestionType'] == 'Tolerance')].reset_index()
            for index, row in toleranceQuestions.iterrows():
                self.questions.append(
                    RiskQuestion(row['QuestionText'],
                                row['QuestionWeight']))
                answers = riskAnswers[(riskAnswers['QuestionID'] ==
                    row['QuestionID'])]
                for indexA, rowA in answers.iterrows():
                    self.questions[index].answers.append(
                        RiskQuestionAnswer(rowA['AnswerText'],
                                            rowA['AnswerValue']))
        else:
            capacityQuestions = riskQuestions[(riskQuestions['QuestionType'] == 'Capacity')].reset_index()
            for index, row in capacityQuestions.iterrows():
                self.questions.append(
                        RiskQuestion(row['QuestionText'],
                                    row['QuestionWeight']))
                answers = riskAnswers[(
                    riskAnswers['QuestionID'] == row['QuestionID'])]
                for indexA, rowA in answers.iterrows():
                    self.questions[index].answers.append(
                        RiskQuestionAnswer(rowA['AnswerText'],
                                            rowA['AnswerValue']))
                    


    def answerQuestionnaire(self):
        for i in range(len(self.questions)):
            question = self.questions[i]
            print(question.questionText)
            for n in range(len(question.answers)):
                answer = question.answers[n]
                print(str(n) + ":" + answer.answerText)
            nChosen = int(input("Pick a answer between 0 and " + str(len(question.answers)-1)+":"))
            self.questions[i].answers[nChosen].selected = True
            print("\n")

    def calculateScore(self):
        print("Risk Score:")
        myTotalScore = 0
        for question in self.questions:
            for answer in question.answers:
                if (answer.selected == True):
                    myTotalScore = myTotalScore + (
                        answer.score * question.weight)
                    print(answer.answerText + ": " + str(
                        answer.score * question.weight))
        print("Total Risk Score: " + str(myTotalScore) + "\n")
        self.score = myTotalScore








 
            