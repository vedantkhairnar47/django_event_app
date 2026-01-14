from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['user']
        fields = ['name', 'date', 'time', 'description']

        def clean(self):
            cleaned_data = super().clean()
            date = cleaned_data.get('date')
            time = cleaned_data.get('time')

            # user is passed from the view
            user = self.instance.user if self.instance.pk else self.initial.get('user')

            if date and time and user:
                conflict = Event.objects.filter(
                    user=user,
                    date=date,
                    time=time
                )

                # Exclude current event while updating
                if self.instance.pk:
                    conflict = conflict.exclude(pk=self.instance.pk)

                if conflict.exists():
                    raise forms.ValidationError(
                        "You already have an event scheduled at this date and time."
                    )

            return cleaned_data
