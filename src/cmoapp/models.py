"""All models for myapp Django application.
"""
from django.db import models

#all models have automatically add an auto-increment id unless another field is explicitly specified as primary key
#note, on_delete assigns a Function 'Callback'
#note, no fking clue in the django tutorial that says you can add a null option, only says field options are
#avaliable to all field types, but no explict example wtf
#note, if you want a FK that is null, you have to set blank=true so that validation will not be triggered

class Account(models.Model):
    TYPES = (
        ('Analyst','Analyst'),
        ('Operator', 'Operator'),
        ('Chief', 'Chief')
    )
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=1024)
    type = models.CharField(max_length=20, choices=TYPES)

    def __str__(self):
        return '{}'.format(self.login)

class CrisisType(models.Model):
    #Attributes
    name = models.CharField(max_length=50)
    def __str__(self):
        return '{}'.format(self.name)

#has nothing but a bunch of foreign keys such keys much wow
#Crisis ID
class Crisis(models.Model):
    #analyst is FK to crisis. This enables analyst to be deleted once the crisis is resolved
    analyst = models.OneToOneField(Account,blank=True,null=True,limit_choices_to={'type':'Analyst'}, on_delete=models.SET_NULL)
    STATUS = (
        ('Clean-up','Clean up'),
        ('Ongoing','Ongoing'),
        ('Resolved', 'Resolved')
    )
    status = models.CharField(max_length=20, choices=STATUS)

    #class Meta:
     #   ordering = ['analyst']

    def injuries(self):
        return self.efupdate_set.latest('datetime').totalDeaths

    def deaths(self):
        return self.efupdate_set.latest('datetime').totalInjured

    def __str__(self):
        return 'ID: {} - assigned to: {}'.format(self.pk, self.analyst)

class CrisisReport(models.Model):
    #attributes
    description = models.TextField()
    datetime = models.DateTimeField()
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
    radius = models.IntegerField(verbose_name="Radius(Metres)")
    #Relations, can have no crisis assigned for the sake of testi

    crisis = models.ForeignKey(Crisis,null=True,blank=True,on_delete=models.CASCADE)
    crisisType = models.ForeignKey(CrisisType,null=True,blank=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return 'ID: {} - {}'.format(self.pk,self.description)

#The response plan of the crsis.
#The deployment id is the action plan id
class ActionPlan(models.Model):
    #attributes
    description = models.TextField(null=True,blank=True)
    STATUS= (
        ('Planning','Planning'),
        ('CORequest','Awaiting CO Approval'),
        ('PMORequest','Awaiting PMO Approval'),
        ('Rejected','Rejected'),
        ('PMOApproved','Approved')
    )
    status = models.CharField(max_length=20, choices=STATUS)
    COComments = models.TextField(null=True)
    PMOComments = models.TextField(null=True)
    resolutionTime = models.DurationField()
    projectedCasualties = models.DecimalField(max_digits=5, decimal_places=2)
    #Relations
    TYPES = (
        ('Clean-up','Clean up'),
        ('Combat','Combat'),
        ('Resolved','Resolved')
    )
    type = models.CharField(max_length=20, choices=TYPES)
    crisis = models.ForeignKey(Crisis, on_delete= models.CASCADE)

    def abridged_description(self):
        return self.description[70].append("...")

    def __str__(self):
        return 'ID: {}'.format(self.pk);

class Force(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    #Current Utilisation can be NULL, in the event that EF cannot provide, then the field is set to NULL and Blank
    currentUtilisation = models.DecimalField(null=True,blank=True, max_digits=5, decimal_places=2)
    def __str__(self):
        return '{}'.format(self.name);

class ForceDeployment(models.Model):
    #a force can only be deleted after all force deployments are deleted
    name = models.ForeignKey(Force, on_delete= models.PROTECT)
    recommended = models.DecimalField(max_digits=5, decimal_places=2)
    max = models.DecimalField(max_digits=5, decimal_places=2)
    actionPlan =  models.ForeignKey(ActionPlan, on_delete= models.CASCADE)
    def __str__(self):
        return 'ID: {} Name: {}'.format(self.pk,self.name);

class EFUpdate(models.Model):
    #Attributes
    datetime = models.DateTimeField()
    affectedRadius = models.DecimalField(max_digits=12,decimal_places=2, verbose_name="Affected Radius")
    totalInjured = models.IntegerField(verbose_name="Total Injured")
    totalDeaths = models.IntegerField(verbose_name="Total Deaths")
    duration =  models.DurationField()
    actionPlan = models.ForeignKey(ActionPlan,null=True,on_delete = models.SET_NULL)
    #i leave this here in case the action plan can be deleted. we can thus still have a reference back to cris
    crisis = models.ForeignKey(Crisis, on_delete =  models.CASCADE)
    description = models.TextField()
    #We are removing types and adding a request
    TYPES = (
        ('Request','Request'),
        ('Notifications','Notifications')
    )
    def __str__(self):
        return 'ID: {}'.format(self.pk)

class ForceUtilization(models.Model):
    name = models.ForeignKey(Force,on_delete= models.CASCADE)
    utilization = models.DecimalField(max_digits=5, decimal_places=2)
    update = models.ForeignKey(EFUpdate, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name);