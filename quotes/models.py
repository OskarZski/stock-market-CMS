from django.db import models

class Stock(models.Model):
	ticker = models.CharField(max_length=10)
	# holdings = models.DecimalField(max_digits=10, decimal_places=5)
	shares_owned = models.PositiveIntegerField(default=0)
	
	def __str__(self):
		return self.ticker