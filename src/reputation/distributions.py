class Distribution:
    def __init__(self, name, amount):
        self._name = name
        self._amount = amount

    @property
    def name(self):
        return self._name

    @property
    def amount(self):
        return self._amount


CreatePaper = Distribution(
    'CREATE_PAPER', 1
)

CommentEndorsed = Distribution(
    'COMMENT_ENDORSED', 15
)
CommentFlagged = Distribution(
    'COMMENT_FLAGGED', -2
)
CommentUpvoted = Distribution(
    'COMMENT_UPVOTED', 5
)
CommentDownvoted = Distribution(
    'COMMENT_DOWNVOTED', -1
)

ReplyEndorsed = Distribution(
    'REPLY_ENDORSED', 15
)
ReplyFlagged = Distribution(
    'REPLY_FLAGGED', -2
)
ReplyUpvoted = Distribution(
    'REPLY_UPVOTED', 5
)
ReplyDownvoted = Distribution(
    'REPLY_DOWNVOTED', -1
)

ThreadEndorsed = Distribution(
    'THREAD_ENDORSED', 15
)
ThreadFlagged = Distribution(
    'THREAD_FLAGGED', -2
)
ThreadUpvoted = Distribution(
    'THREAD_UPVOTED', 5
)
ThreadDownvoted = Distribution(
    'THREAD_DOWNVOTED', -1
)

SummaryApproved = Distribution(
    'SUMMARY_APPROVED', 15
)
SummaryRejected = Distribution(
    'SUMMARY_REJECTED', -2
)
SummaryFlagged = Distribution(
    'SUMMARY_FLAGGED', -5
)