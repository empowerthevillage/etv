from django.db import models
from datetime import date

from phonenumber_field.modelfields import PhoneNumberField

STATE_CHOICES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)


class Flyer(models.Model):
    state                   = models.CharField(choices=STATE_CHOICES, blank=True, null=True, max_length=120)
    year                    = models.PositiveIntegerField(default=int(date.today().year))
    thumbnail_link          = models.URLField(blank=True, null=True)
    pg2_link                = models.URLField(blank=True, null=True)
    pdf_link                = models.URLField(blank=True, null=True)
    active                  = models.BooleanField(default=True)
    order                   = models.IntegerField(default=1)
    
    def __str__(self):
        return '%s %s OBB Flyer' %(self.state, self.year)

    class Meta:
        ordering = ['order', 'state']
        
class VillageStriversApplication(models.Model):
    first_name              = models.CharField(blank=True, null=True, max_length=120)
    last_name               = models.CharField(blank=True, null=True, max_length=120)
    email                   = models.EmailField(blank=True, null=True)
    phone                   = PhoneNumberField(blank=True, null=True)
    school_classification   = models.CharField(blank=True, null=True, max_length=120)
    resume                  = models.FileField(blank=True, null=True)
    interest                = models.CharField(blank=True, null=True, max_length=120)
    category                = models.CharField(blank=True, null=True, max_length=120)
    open_to_unpaid          = models.CharField(blank=True, null=True, max_length=120, verbose_name='Open to unpaid internships/apprenticeships')
    submitted               = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return 'Village Strivers Application - %s %s' %(self.first_name, self.last_name)