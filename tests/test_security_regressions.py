import pytest
from agents.base import AuditTrail
from agents.llm_factory import LLMFactory
from agents.models import SystemTaskPayload


def test_sanitization_cannot_erase_required_id():
    with pytest.raises(ValueError):
        SystemTaskPayload(task_id="\n\t", target_identifier="VESSEL", primary_metric=1)


def test_audit_trail_snapshot_cannot_mutate_chain():
    audit = AuditTrail(secret_key="unit-test-secret")
    audit.log("tester", "test", "event", {"id": "A"})
    snapshot = audit.get_trail()
    snapshot.clear()
    assert len(audit.get_trail()) == 1
    assert audit.verify_integrity()
    snapshot = audit.get_trail()
    snapshot[0]["current_hash"] = "altered"
    assert audit.verify_integrity()


def test_mock_provider_discloses_absence_of_analysis():
    engine = LLMFactory.create("mock")
    reply = engine.invoke("How is the reactor?")
    assert "No scientific or LLM analysis performed" in reply


@pytest.mark.parametrize("provider", ["openai", "claude", "ollama", "unrecognized"])
def test_unimplemented_providers_are_not_silently_mocked(provider):
    with pytest.raises(ValueError):
        LLMFactory.create(provider)
