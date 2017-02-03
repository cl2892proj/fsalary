from __future__ import unicode_literals

from django.db import models

# Create your models here.

from mptt.models import MPTTModel, TreeForeignKey
from django_comments.models import CommentAbstractModel

class MPTTComment(MPTTModel, CommentAbstractModel):
    """
    Threaded comments - add support for the parent comment store and MPTT traversal
    """
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        # comments on one level will be ordered by date of creation
        order_insertion_by = ['submit_date']

    class Meta:
        ordering = ['tree_id', 'lft']
