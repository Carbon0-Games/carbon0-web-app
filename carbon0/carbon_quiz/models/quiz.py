from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

from carbon_quiz.models.mission import Mission
from carbon_quiz.models.question import Question


class Quiz(models.Model):
    """Represents a collection of 5 questions given to the user."""

    title = models.CharField(
        max_length=500, unique=True, help_text="Title of the quiz.", null=True
    )
    slug = models.SlugField(
        max_length=500,
        blank=True,
        editable=False,
        null=True,
        help_text=(
            "Unique URL path to access this quiz. " + "Generated by the system."
        ),
    )
    questions = ArrayField(
        models.IntegerField(),
        size=5,
        help_text="Array of ids for the quiz questions.",
        null=True,
        blank=True,
    )
    active_question = models.IntegerField(
        help_text="Id of the question currently being asked.", default=0, blank=True
    )
    carbon_value_total = models.FloatField(
        blank=True,
        default=1000,
        help_text="Total metric tons of carbon that the user can eliminate.",
    )
    open_response_answers = ArrayField(
        models.TextField(null=True, blank=True, help_text="User's response."),
        default=list
    )

    def __str__(self):
        """Returns human-readable name of the Quiz."""
        return f"{self.title}"

    def get_absolute_url(self):
        """
        Returns a fully qualified path for a Quiz.
        The arg for question_answered on first GET after QuizCreate, is 0
        because we want to make sure it can't refer to a real Question model.
        """
        path_components = {
            "slug": self.slug,
            # for the question number, increment zero-indexed number
            "question_number": self.active_question + 1,
        }
        return reverse("carbon_quiz:quiz_detail", kwargs=path_components)

    def increment_carbon_value(self, question):
        """
        Increase the total carbon value of this Quiz model, by the individual
        carbon_value field of one of the Question model instances.

        Parameter:
        question(Question): a Question instance

        Returns: None

        """
        self.carbon_value_total += question.carbon_value
        self.save()
        return None

    def increment_active_question(self):
        """Moves us to the next Question, in the questions array."""
        self.active_question += 1
        self.save()

    def save(self, *args, **kwargs):
        """Creates a URL safe slug automatically when a new note is saved."""
        if not self.pk:
            self.slug = slugify(self.title, allow_unicode=True)

        # call save on the superclass
        return super().save(*args, **kwargs)

    def get_current_question(self):
        """Return the Question which is current active in this Quiz."""
        question_id = self.questions[self.active_question]
        question_obj = Question.objects.get(id=question_id)
        return question_obj

    def get_related_missions(self):
        """Return Missions related to the Questions on a Quiz."""
        missions = list()
        # get the question id that each user actually interacted with
        for question_id in self.questions:
            # check if this question was answered no (needs a mission)
            if question_id > 0:
                # get a mission related to the Question
                question_obj = Question.objects.get(id=question_id)
                mission = Mission.get_related_mission(question_obj)
                # add to the list of Missions
                missions.append(mission)
        return missions

    def get_unrelated_missions(self):
        """
        Return Missions related to the Question for which the user 
        does not necessarily need to improve.
        """
        # get all the ids of all Questions, removing affirmative ones
        not_improvement_questions = (
            Question.objects.exclude(pk__in=self.questions)
        )
        # randomly sample missions
        missions = list()
        for question_obj in not_improvement_questions:
            mission = Mission.get_related_mission(question_obj)
            missions.append(mission)
        return missions
