from django import forms
from .models import *

from crispy_forms.helper import FormHelper 
from crispy_forms.layout import Submit, Layout, Hidden

class NewPost(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(NewItem, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-exampleForm"
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        # self.helper.layout = Layout(
        #     Hidden('user', "rst0")
        #     )   

        self.helper.add_input(Submit('submit', 'Submit'))
                
    class Meta:
        model = Post
        exclude = ('user', 'likes')
        #fields =  "__all__" #('item', 'image', 'description', 'starting_bid', 'item_category')
        # labels = {
        #     'staring_bid': 'Starting bid in £ GBP',
        # }

class NewFollow(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(NewItem, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "id-exampleForm"
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        # self.helper.layout = Layout(
        #     Hidden('user', "rst0")
        #     )   

    #    self.helper.add_input(Submit('submit', 'Submit'))
                
    class Meta:
        model = Post
        #exclude = ('user', 'likes')
        fields =  "__all__" #('item', 'image', 'description', 'starting_bid', 'item_category')
        # labels = {
        #     'staring_bid': 'Starting bid in £ GBP',
        # }
