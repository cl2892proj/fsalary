
def get_model():
    from my_comment_app.models import MPTTComment
    return MPTTComment

def get_form():
    from my_comment_app.forms import MPTTCommentForm
    return MPTTCommentForm
