from __future__ import annotations

from datetime import date

from ai_providers.base import AIProvider
from incident_timeline_extractor.timeline.model import Timeline
from incident_timeline_extractor.timeline.serializer import timeline_to_markdown
from postmortem_generator_ai.model import ActionItem, Postmortem


def _fallback_postmortem(timeline: Timeline, engineer_input: str, language: str) -> dict:
    services = {e.service for e in timeline.events if e.service}
    major_services = ", ".join(sorted(services)) or "unknown"
    return {
        "title": f"Postmortem for {timeline.incident_id}",
        "summary": engineer_input or f"Incident {timeline.incident_id}",
        "impact": f"Affected services: {major_services}.",
        "root_cause": "Root cause under investigation.",
        "contributing_factors": "To be refined.",
        "what_went_well": "Detection pipeline worked.",
        "what_can_be_improved": "Automate remediation and alert routing.",
        "lessons_learned": "Keep timelines consistent.",
        "action_items": [
            {
                "description": "Add detailed runbooks",
                "owner": "team",
                "due_date": None,
                "status": "open",
            }
        ],
    }


def generate_postmortem(
    timeline: Timeline,
    engineer_input: str,
    provider: AIProvider | None,
    language: str = "en",
) -> Postmortem:
    timeline_md = timeline_to_markdown(timeline)

    prompt = f"""
    Create a blameless SRE postmortem in {language}.
    Incident id: {timeline.incident_id}
    Engineer input: {engineer_input}
    Timeline:\n{timeline_md}
    """

    data: dict
    if provider:
        try:
            data = provider.generate_postmortem(prompt, language)
        except Exception:
            data = _fallback_postmortem(timeline, engineer_input, language)
    else:
        data = _fallback_postmortem(timeline, engineer_input, language)

    if not data.get("action_items"):
        data["action_items"] = [
            {
                "description": "Review monitoring gaps",
                "owner": "sre",
                "due_date": None,
                "status": "open",
            }
        ]

    action_items = [
        ActionItem(
            description=item.get("description", ""),
            owner=item.get("owner"),
            due_date=_parse_due_date(item.get("due_date")),
            status=item.get("status", "open"),
        )
        for item in data.get("action_items", [])
    ]

    return Postmortem(
        incident_id=timeline.incident_id,
        title=data.get("title", f"Postmortem {timeline.incident_id}"),
        date=date.today(),
        severity=timeline.metadata.get("severity", "unknown") if timeline.metadata else "unknown",
        summary=data.get("summary", ""),
        impact=data.get("impact", ""),
        root_cause=data.get("root_cause", ""),
        contributing_factors=data.get("contributing_factors", ""),
        timeline_md=timeline_md,
        what_went_well=data.get("what_went_well", ""),
        what_can_be_improved=data.get("what_can_be_improved", ""),
        action_items=action_items,
        lessons_learned=data.get("lessons_learned", ""),
    )


def _parse_due_date(value):
    if value is None or value == "":
        return None
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except Exception:
        return None


__all__ = ["generate_postmortem"]
