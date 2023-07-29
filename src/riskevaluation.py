"""
This module creates the risk questionnaire for onboarding 
and evaluating clients.
"""

#!/usr/bin/env python #

import pandas as pd


class RiskEvaluation:
    """
    Performs the risk evaluation process and
    returns a scores for both risk capacity and tolerance.
    """

    def __init__(self):
        risk_file_dir = "../data/questionnaire.csv"
        risk_ans_dir = "../data/answers.csv"

        self.tolerance_evaluation = RiskQuestionnaire()
        self.capacity_evaluation = RiskQuestionnaire()

        self.tolerance_evaluation.load_questionnaire(
            risk_file_dir, risk_ans_dir, "Tolerance"
        )
        self.capacity_evaluation.load_questionnaire(
            risk_file_dir, risk_ans_dir, "Capacity"
        )


class RiskQuestion:
    """
    A question about risk posed to a client.
    """

    def __init__(self, question_text, weight=1):
        self.question_text = question_text
        self.weight = weight
        self.answers = []


class RiskQuestionAnswer:
    """
    A client answer to a question regarding risk
    """

    def __init__(self, answer_text, score, selected=False):
        self.answer_text = answer_text
        self.score = score
        self.selected = selected


class RiskQuestionnaire:
    """
    Questionairre of risk based questions posed to a client or user.
    """

    def __init__(self):
        self.questions = []
        self.score = 0

    def load_questionnaire(
        self, risk_questions_file_name, risk_answers_file_name, question_type
    ):
        """
        Loads the questionnaire for the user
        """
        if question_type not in ["Tolerance", "Capacity"]:
            raise ValueError("Type must be Tolerance or Capacity.")

        risk_questions = pd.read_csv(risk_questions_file_name).reset_index()
        risk_answers = pd.read_csv(risk_answers_file_name).reset_index()
        if question_type == "Tolerance":
            tolerance_questions = risk_questions[
                (risk_questions["QuestionType"] == "Tolerance")
            ].reset_index()
            for index, row in tolerance_questions.iterrows():
                self.questions.append(
                    RiskQuestion(row["QuestionText"], row["QuestionWeight"])
                )
                answers = risk_answers[
                    (risk_answers["QuestionID"] == row["QuestionID"])
                ]
                for _, row_a in answers.iterrows():
                    self.questions[index].answers.append(
                        RiskQuestionAnswer(row_a["AnswerText"], row_a["AnswerValue"])
                    )

        else:
            capacity_questions = risk_questions[
                (risk_questions["QuestionType"] == "Capacity")
            ].reset_index()
            for index, row in capacity_questions.iterrows():
                self.questions.append(
                    RiskQuestion(row["QuestionText"], row["QuestionWeight"])
                )
                answers = risk_answers[
                    (risk_answers["QuestionID"] == row["QuestionID"])
                ]
                for _, row_a in answers.iterrows():
                    self.questions[index].answers.append(
                        RiskQuestionAnswer(row_a["AnswerText"], row_a["AnswerValue"])
                    )

    def answer_questionnaire(self):
        """
        Function called to loop through questions and record answers from users.
        """
        for i, question in enumerate(self.questions):
            print(question.question_text)
            for j, answer in enumerate(question.answers):
                print(f"{j}:{answer.answer_text}")
            n_chosen = int(
                input(f"Pick an answer between 0 and {len(question.answers) - 1}:")
            )
            self.questions[i].answers[n_chosen].selected = True
            print("\n")

    def calculate_score(self):
        """
        Compute score based on user input
        """
        print("Risk Score:")
        my_total_score = 0
        for question in self.questions:
            for answer in question.answers:
                if answer.selected is True:
                    my_total_score = my_total_score + (answer.score * question.weight)
                    print(
                        answer.answer_text + ": " + str(answer.score * question.weight)
                    )
        print("Total Risk Score: " + str(my_total_score) + "\n")
        self.score = my_total_score

        return self.score
