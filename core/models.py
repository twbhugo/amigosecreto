from django.db import models

#FamilyGroup model to group guests by family.
class FamilyGroup(models.Model):
    family_group_id = models.AutoField(primary_key=True)
    family_name = models.CharField(max_length=100)

    def __str__(self):
        return self.family_name

#This model represents a guest attending the event.
class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)
    family_group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='guests', null=True, blank=True)
    name = models.CharField(max_length=100)
    pin = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    secret_friend = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    ideal_gift = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    hashed_pin = models.CharField(max_length=255, null=True, blank=True)
    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

#Model to assign secret friends and designate ideal gifts.
class SecretFriendAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    giver = models.ForeignKey(Guest, related_name='given_assignments', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Guest, related_name='received_assignments', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.giver.name} -> {self.receiver.name}"