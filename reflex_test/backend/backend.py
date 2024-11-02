# Imports

import reflex as rx
import google.generativeai as genai

from decouple import config
import json

# End Imports


class User(rx.Model, table=True):
    """The User model."""

    ip_address: str
    total_correct_answers: int = 0
    total_wrong_answers: int = 0


class State(rx.State):

    """The app state."""

    current_user: User = User()

    start_quiz = 0

    # User scores

    correct_answers = 0
    wrong_answers = 0

    selected_option: str = ""
    question_text: str = "Question Text"
    question_options: list[str] = [1, 2, 3, 4]
    question_answer: str = ""
    question_loading: bool = True
    question_code_part: str = ""
    message: str = ''

    # Start button
    player_icon_class: str = 'play'
    player_button_text: str = 'Start Playing'
    player_button_color: str = '#1f550e'

    # Method to set the selected option
    def set_option(self, option: str) -> None:

        """
        Set selected option
        """

        self.selected_option = option

    async def submit_selection(self) -> None:

        """
        Submit selection and check if selection is correct.
        If correct:
            += Correct answers
        Else:
            += Wrong answers
        """

        if self.selected_option == self.question_answer and not self.selected_option == "":
            self.correct_answers += 1
            yield rx.toast.success("Congratulations! Correct answer.", position='top-right')
        elif self.selected_option != self.question_answer and not self.selected_option == "":
            self.wrong_answers += 1
            yield rx.toast.error("Ahh, Wrong answer!", position='top-right')
        else:
            yield rx.toast.warning("Please click next question!", position='top-right')

        await self.reset_question()

        # Enable when user update process is fixed
        await self.get_or_set_user_data("update")

    async def get_or_set_user_data(self, section='init') -> None:

        """
        Update user correct and wrong answers
        """

        with rx.session() as session:

            # Get user
            user = session.exec(
                User.select().where(
                    (User.ip_address == self.router.session.client_ip)
                )
            ).first()

            # If user data
            if user:

                # If from quiz start section set initial value as user db saved value
                if section == 'init':
                    self.correct_answers = user.total_correct_answers
                    self.wrong_answers = user.total_wrong_answers

                user.total_correct_answers = self.correct_answers
                user.total_wrong_answers = self.wrong_answers
                session.add(user)
                session.commit()
            else:

                # Else create user data
                session.add(
                    User(
                        ip_address=self.router.session.client_ip,
                        total_correct_answers=self.correct_answers,
                        total_wrong_answers=self.wrong_answers
                    )
                )
                session.commit()

    async def reset_question(self) -> None:

        """
        Reset question and it's relative data
        """

        self.question_text = ''
        self.question_options = []
        self.question_answer = ''
        self.question_code_part = ''
        self.selected_option = ''
        self.message = 'Please click next question'

    async def fetch_question(self) -> None:

        """
        Fetch question
        """

        # Clear the previous selected item
        self.message = ''
        self.selected_option = ""
        self.question_loading = True

        requirements = """
        Generate python language related quiz question with 4 options. Return your response in json format.
        The format should be exact as below:
        {
            'question': 'question_text',
            'options':['option 1', 'option 2','option 3', 'option 4'],
            'answer': 'option 1'
        }
        Avoid json prefix as it throws error while converting to native python dict object.
        Do not give any markdown edits or styling as it may cause error while decoding.
        And all string should start and close with double quotes, not single. Make the questions little harder.
        """

        # API configuration
        GOOGLE_API_KEY = config('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)

        # Initializing the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=[])

        # Safe calling for model call and json loading the response
        try:
            message = chat.send_message(requirements)
            response = json.loads(message.text)
        except:
            message = chat.send_message(requirements + " Output in json format not any others and fix the error.")
            response = json.loads(message.text)

        # Safe splitter of question and coding part
        try:
            question = response['question'].split('```')
            self.question_text = question[0]
            self.question_code_part = f'```python {question[1]}```'
        except:
            self.question_text = response['question']

        # Setting options and answer
        self.question_options = response['options']
        self.question_answer = response['answer']

        self.question_loading = False

    async def enable_quiz(self) -> None:

        """
        Enable quiz container
        """

        # Bitwise operator or enabling disabling the quiz section
        self.start_quiz ^= 1

        # To avoid error setting initial values as 0
        self.wrong_answers = 0
        self.correct_answers = 0

        # Get user data
        await self.get_or_set_user_data("init")

        # Set button state and fetch question based on event
        if self.start_quiz:
            self.player_icon_class = 'pause'
            self.player_button_text = 'Stop Playing'
            self.question_loading = True
            await self.fetch_question()
        else:
            self.player_icon_class = 'play'
            self.player_button_text = 'Start Playing'

