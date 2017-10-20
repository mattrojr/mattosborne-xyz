from django.forms import ModelForm, Form
from .models import *

class CampaignForm(ModelForm):
    class Meta:
        model = Campaign
        fields = [
            'name',
            'description',
        ]


class GameMasterForm(ModelForm):
    class Meta:
        model = GameMaster
        fields = [
            'user',
            'campaign',
        ]


class AreaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        campaign = kwargs.pop('campaign')
        super(AreaForm, self).__init__(*args, **kwargs)
        try:
            instance = kwargs['instance']
            parent_list = Area.objects.filter(campaign=campaign).difference(instance.get_descendants(),
                                                                            Area.objects.filter(id=instance.id))

        except:
            parent_list = Area.objects.filter(campaign=campaign)
        self.fields['parent'].queryset = parent_list

    class Meta:
        model = Area
        fields = [
            'code',
            'name',
            'description',
            'notes',
            'parent',
        ]