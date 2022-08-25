import json

import requests
from django.core.management.base import BaseCommand

from discussion.models import Comment, Reply, Thread, Vote
from hypothesis.models import Hypothesis
from paper.models import Paper
from purchase.models import Purchase
from reputation.models import Bounty
from researchhub.settings import AMPLITUDE_API_KEY
from researchhub_document.models import ResearchhubPost
from user.models import User
from utils.parsers import json_serial

API_URL = "https://api.amplitude.com/2/httpapi"


class Command(BaseCommand):
    def get_user_props(self, user):
        if user.is_anonymous:
            user_properties = {
                "email": "",
                "first_name": "Anonymous",
                "last_name": "Anonymous",
                "reputation": 0,
                "is_suspended": False,
                "probable_spammer": False,
                "invited_by_id": 0,
                "is_hub_editor": False,
            }
            user_id = "_Anonymous_"
        else:
            invited_by = user.invited_by
            if invited_by:
                invited_by = invited_by.id
            user_properties = {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "reputation": user.reputation,
                "is_suspended": user.is_suspended,
                "probable_spammer": user.probable_spammer,
                "invited_by_id": invited_by,
                "is_hub_editor": user.is_hub_editor(),
            }
            user_id = f"user: {user.email}_{user.id}"
        return user_id, user_properties

    def forward_amp_event(self, events):
        event_data = {"api_key": AMPLITUDE_API_KEY, "events": events}
        data = json.dumps(event_data, default=json_serial)
        headers = {"Content-Type": "application/json", "Accept": "*/*"}
        request = requests.post(API_URL, data=data, headers=headers)
        res = request.json()
        if request.status_code != 200:
            res = request.json()
            print(res)
        print(res)

    def handle_comments(self, comments):
        print("Comments")
        count = comments.count()
        events = []
        for i, comment in enumerate(comments.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = comment.created_by
                user_id, user_properties = self.get_user_props(user)
                if comment.unified_document == "PAPER":
                    event_type = "paper_thread_comments_create"
                elif comment.unified_document == "HYPOTHESIS":
                    event_type = "hypothesis_thread_comments_create"
                else:
                    event_type = "post_thread_comments_create"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(comment.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{comment.id}",
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_replies(self, replies):
        print("Replies")
        count = replies.count()
        events = []
        for i, reply in enumerate(replies.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = reply.created_by
                user_id, user_properties = self.get_user_props(user)
                if reply.unified_document == "PAPER":
                    event_type = "paper_thread_comment_replies_create"
                elif reply.unified_document == "HYPOTHESIS":
                    event_type = "hypothesis_thread_comment_replies_create"
                else:
                    event_type = "post_thread_comment_replies_create"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(reply.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{reply.id}",
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_threads(self, threads):
        print("Threads")
        count = threads.count()
        events = []
        for i, thread in enumerate(threads.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = thread.created_by
                user_id, user_properties = self.get_user_props(user)
                if thread.unified_document == "PAPER":
                    event_type = "paper_threads_create"
                elif thread.unified_document == "HYPOTHESIS":
                    event_type = "hypothesis_threads_create"
                else:
                    event_type = "post_threads_create"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(thread.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{thread.id}",
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_papers(self, papers):
        print("Papers")
        count = papers.count()
        events = []
        for i, paper in enumerate(papers.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = paper.uploaded_by
                user_id, user_properties = self.get_user_props(user)
                event_type = "paper_create"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(paper.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{paper.id}",
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_new_flow_papers(self, papers):
        print("Papers")
        count = papers.count()
        events = []
        for i, paper in enumerate(papers.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = paper.uploaded_by
                user_id, user_properties = self.get_user_props(user)
                event_type = "paper_submission_create"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(paper.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{paper.submission.id}",
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_hypotheses(self, hypotheses):
        print("Hypotheses")
        count = hypotheses.count()
        events = []
        for i, hypothesis in enumerate(hypotheses.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = hypothesis.created_by
                user_id, user_properties = self.get_user_props(user)
                event_type = "hypothesis_create"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(hypothesis.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{hypothesis.id}",
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_posts(self, posts):
        print("Posts")
        count = posts.count()
        events = []
        for i, post in enumerate(posts.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = post.created_by
                user_id, user_properties = self.get_user_props(user)
                event_type = "researchhub_post_create"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(post.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{post.id}",
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_votes(self, votes):
        print("Votes")
        count = votes.count()
        events = []
        for i, vote in enumerate(votes.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                vote_content_type = vote.content_type
                vote_type = "upvote" if vote.vote_type == 1 else "downvote"
                try:
                    if vote_content_type.model == "paper":
                        event_type = f"paper_{vote_type}"
                    elif vote_content_type.model == "hypothesis":
                        event_type = f"hypothesis_{vote_type}"
                    elif vote_content_type.model == "researchhubpost":
                        event_type = f"researchhub_post_{vote_type}"
                    elif vote_content_type.model == "thread":
                        vote_item = vote.item
                        if not vote.item:
                            continue
                        else:
                            parent_doc_type = vote_item.unified_document.document_type
                            if parent_doc_type == "PAPER":
                                parent_class = "paper"
                            elif parent_doc_type == "HYPOTHESIS":
                                parent_class = "hypothesis"
                            else:
                                parent_class = "researchhubpost"
                            event_type = f"{parent_class}_threads_{vote_type}"
                    elif vote_content_type.model == "comment":
                        vote_item = vote.item
                        if not vote.item:
                            continue
                        else:
                            parent_doc_type = vote_item.unified_document.document_type
                            if parent_doc_type == "PAPER":
                                parent_class = "paper"
                            elif parent_doc_type == "HYPOTHESIS":
                                parent_class = "hypothesis"
                            else:
                                parent_class = "researchhubpost"
                            event_type = f"{parent_class}_thread_comments_{vote_type}"
                    elif vote_content_type.model == "reply":
                        vote_item = vote.item
                        if not vote.item:
                            continue
                        else:
                            parent_doc_type = vote_item.unified_document.document_type
                            if parent_doc_type == "PAPER":
                                parent_class = "paper"
                            elif parent_doc_type == "HYPOTHESIS":
                                parent_class = "hypothesis"
                            else:
                                parent_class = "researchhubpost"
                            event_type = (
                                f"{parent_class}_thread_comment_replies_{vote_type}"
                            )
                    else:
                        continue
                except Exception as e:
                    print(e)
                    continue
                user = vote.created_by
                user_id, user_properties = self.get_user_props(user)
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(vote.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{vote.id}",
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_user_signup(self, users):
        print("Users")
        count = users.count()
        events = []
        for i, user in enumerate(users.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user_id, user_properties = self.get_user_props(user)
                event_type = "user_signup"
                hit = {
                    "user_id": user_id,
                    "event_type": "user_signup",
                    "time": int(user.date_joined.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{user.id}",
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_purchases(self, purchases):
        print("Purchases")
        count = purchases.count()
        events = []
        for i, purchase in enumerate(purchases.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = purchase.user
                user_id, user_properties = self.get_user_props(user)
                event_type = "purchase_create"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(purchase.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{purchase.id}",
                    "event_properties": {
                        "interaction": purchase.purchase_method,
                        "amount": purchase.amount,
                        "object_id": purchase.object_id,
                        "content_type": purchase.content_type.model,
                    },
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_bounties(self, bounties):
        print("bounties")
        count = bounties.count()
        events = []
        for i, bounty in enumerate(bounties.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = bounty.created_by
                user_id, user_properties = self.get_user_props(user)
                event_type = "bounty_create"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(bounty.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{bounty.id}",
                    "event_properties": {
                        "amount": bounty.amount,
                    },
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle_closed_bounties(self, bounties):
        print("bounties")
        count = bounties.count()
        events = []
        for i, bounty in enumerate(bounties.iterator()):
            if (i % 1000 == 0 and i != 0) or (count - 1) == i:
                self.forward_amp_event(events)
                events = []
            else:
                print(f"{i}/{count}")
                user = bounty.created_by
                user_id, user_properties = self.get_user_props(user)
                event_type = "bounty_approve_bounty"
                hit = {
                    "user_id": user_id,
                    "event_type": event_type,
                    "time": int(bounty.created_date.timestamp()),
                    "user_properties": user_properties,
                    "insert_id": f"{event_type}_{bounty.id}",
                    "event_properties": {
                        "amount": bounty.amount,
                    },
                }
                events.append(hit)
        self.forward_amp_event(events)

    def handle(self, *args, **options):
        papers = Paper.objects.filter(
            uploaded_by__isnull=False, submission__isnull=True
        )
        new_flow_papers = Paper.objects.filter(
            uploaded_by__isnull=False, submission__isnull=False
        )
        hypotheses = Hypothesis.objects.filter(created_by__isnull=False)
        posts = ResearchhubPost.objects.filter(created_by__isnull=False)
        purchases = Purchase.objects.filter(user__isnull=False)
        bounties = Bounty.objects.filter(created_by__isnull=False)
        closed_bounties = Bounty.objects.filter(
            created_by__isnull=False, status="CLOSED"
        )
        user = User.objects.all()
        threads = Thread.objects.filter(created_by__isnull=False)
        comments = Comment.objects.filter(created_by__isnull=False)
        replies = Reply.objects.filter(created_by__isnull=False)
        votes = Vote.objects.filter(created_by__isnull=False)

        # self.handle_threads(threads)
        # self.handle_comments(comments)
        # self.handle_replies(replies)
        # self.handle_papers(papers)
        # self.handle_new_flow_papers(new_flow_papers)
        # self.handle_hypotheses(hypotheses)
        # self.handle_posts(posts)
        self.handle_votes(votes)
        self.handle_user_signup(user)
        self.handle_purchases(purchases)
        self.handle_bounties(bounties)
        self.handle_closed_bounties(closed_bounties)
