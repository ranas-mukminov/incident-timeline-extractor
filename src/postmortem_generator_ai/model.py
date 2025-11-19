from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional


@dataclass
class ActionItem:
    description: str
    owner: Optional[str] = None
    due_date: Optional[date] = None
    status: str = "open"  # open, in_progress, done


@dataclass
class Postmortem:
    incident_id: str
    title: str
    date: date
    severity: str
    summary: str
    impact: str
    root_cause: str
    contributing_factors: str
    timeline_md: str
    what_went_well: str
    what_can_be_improved: str
    action_items: List[ActionItem] = field(default_factory=list)
    lessons_learned: str = ""


__all__ = ["Postmortem", "ActionItem"]
