from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

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

    def get_current_quiz(self):
        """Return the Question which is current active in this Quiz."""
        question_id = self.questions[self.active_question]
        question_obj = Question.objects.get(id=question_id)
        return question_obj
