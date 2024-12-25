from typing import Dict, List
import asyncio
from datetime import datetime

class NotificationManager:
    def __init__(self):
        self.last_check: Dict[str, datetime] = {}
        self.processed_events: List[str] = []
    
    def format_notification(self, event: Dict) -> str:
        event_type = event.get("type", "")
        repo = event.get("repo", {}).get("name", "")
        actor = event.get("actor", {}).get("login", "")
        
        # Base header for all notifications
        header = f"🔔 **New GitHub Activity!**\n\n"
        
        if event_type == "ForkEvent":
            return (
                f"{header}"
                f"🍴 **Repository Forked!**\n"
                f"📂 **Repo:** `{repo}`\n"
                f"👤 **Forked by:** `{actor}`\n"
                f"⏰ _Fork created just now_"
            )
            
        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action", "")
            issue_title = event.get("payload", {}).get("issue", {}).get("title", "")
            issue_number = event.get("payload", {}).get("issue", {}).get("number", "")
            
            status_emoji = "🟢" if action == "opened" else "🔴" if action == "closed" else "🟡"
            
            return (
                f"{header}"
                f"📝 **Issue {action}!**\n"
                f"{status_emoji} **Status:** `{action}`\n"
                f"📂 **Repo:** `{repo}`\n"
                f"#️⃣ **Issue #{issue_number}**\n"
                f"📌 **Title:** `{issue_title}`\n"
                f"👤 **By:** `{actor}`"
            )
            
        elif event_type == "PushEvent":
            commits = event.get("payload", {}).get("commits", [])
            commit_count = len(commits)
            branch = event.get("payload", {}).get("ref", "").split("/")[-1]
            
            commit_messages = "\n".join(
                f"• {commit['message'][:50]}..." if len(commit['message']) > 50 else f"• {commit['message']}"
                for commit in commits[:3]
            )
            
            return (
                f"{header}"
                f"⚡ **New Push Event!**\n"
                f"📂 **Repo:** `{repo}`\n"
                f"🌿 **Branch:** `{branch}`\n"
                f"👤 **By:** `{actor}`\n"
                f"📊 **Commits:** `{commit_count}`\n\n"
                f"📝 **Latest Changes:**\n{commit_messages}"
            )
            
        elif event_type == "PullRequestEvent":
            action = event.get("payload", {}).get("action", "")
            pr_title = event.get("payload", {}).get("pull_request", {}).get("title", "")
            pr_number = event.get("payload", {}).get("pull_request", {}).get("number", "")
            
            status_emoji = "🟢" if action == "opened" else "🔴" if action == "closed" else "🟡"
            
            return (
                f"{header}"
                f"🔄 **Pull Request {action}!**\n"
                f"{status_emoji} **Status:** `{action}`\n"
                f"📂 **Repo:** `{repo}`\n"
                f"#️⃣ **PR #{pr_number}**\n"
                f"📌 **Title:** `{pr_title}`\n"
                f"👤 **By:** `{actor}`"
            )
            
        elif event_type == "CreateEvent":
            ref_type = event.get("payload", {}).get("ref_type", "")
            ref = event.get("payload", {}).get("ref", "")
            
            return (
                f"{header}"
                f"🎉 **New {ref_type} Created!**\n"
                f"📂 **Repo:** `{repo}`\n"
                f"📌 **{ref_type.title()}:** `{ref}`\n"
                f"👤 **By:** `{actor}`"
            )
            
        elif event_type == "DeleteEvent":
            ref_type = event.get("payload", {}).get("ref_type", "")
            ref = event.get("payload", {}).get("ref", "")
            
            return (
                f"{header}"
                f"🗑️ **{ref_type} Deleted!**\n"
                f"📂 **Repo:** `{repo}`\n"
                f"📌 **{ref_type.title()}:** `{ref}`\n"
                f"👤 **By:** `{actor}`"
            )
            
        elif event_type == "WatchEvent":
            return (
                f"{header}"
                f"⭐ **New Star!**\n"
                f"📂 **Repo:** `{repo}`\n"
                f"👤 **Starred by:** `{actor}`"
            )
        
        # Default format for other events
        return (
            f"{header}"
            f"📢 **Event Type:** `{event_type}`\n"
            f"📂 **Repo:** `{repo}`\n"
            f"👤 **By:** `{actor}`"
        )