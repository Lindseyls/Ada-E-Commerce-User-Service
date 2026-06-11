import json
import pytest
from app.consumers.consumer import process_message



# ─── Helpers ──────────────────────────────────────────────────────────────────

def make_sns_message_body(event_type, payload):
    """Wrap a payload in the SNS envelope format that SQS delivers."""
    return json.dumps({
        "Message": json.dumps({
            "event_type": event_type,
            "payload": payload,
        })
    })

def send_order(queue, order):
    """Send an order.placed event to the moto SQS queue."""
    queue.send_message(
        MessageBody=make_sns_message_body("order.placed", order),
        MessageGroupId="orders",
    )


def send_event(queue, event_type, payload):
    """Send an arbitrary event to the moto SQS queue."""
    queue.send_message(
        MessageBody=make_sns_message_body(event_type, payload),
        MessageGroupId="orders",
    )


# ──────────────────────────────────────────────
# process_message
# ──────────────────────────────────────────────
# @pytest.mark.skip
def test_process_message_order_placed_returns_true(one_user, sample_order, sqs_queue):
    send_order(sqs_queue, sample_order)
    messages = sqs_queue.receive_messages(MaxNumberOfMessages=1)

    result = process_message(messages[0])

    assert result is True

# @pytest.mark.skip
def test_process_message_order_placed_prints_confirmation(one_user, sample_order, sqs_queue, capsys):
    send_order(sqs_queue, sample_order)
    messages = sqs_queue.receive_messages(MaxNumberOfMessages=1)

    process_message(messages[0])

    output = capsys.readouterr().out
    assert one_user.first_name in output
    assert one_user.email in output
    assert str(sample_order["id"]) in output

# @pytest.mark.skip
def test_process_message_unknown_event_type_returns_true(one_user, sample_order, sqs_queue):
    send_event(sqs_queue, "order.cancelled", sample_order)
    messages = sqs_queue.receive_messages(MaxNumberOfMessages=1)

    result = process_message(messages[0])

    assert result is True

# @pytest.mark.skip
def test_process_message_unknown_event_type_skips_confirmation(one_user, sample_order, sqs_queue, capsys):
    send_event(sqs_queue, "order.cancelled", sample_order)
    messages = sqs_queue.receive_messages(MaxNumberOfMessages=1)

    process_message(messages[0])

    output = capsys.readouterr().out
    assert output == ""

# @pytest.mark.skip
def test_processed_message_can_be_deleted_from_sqs(one_user, sample_order, sqs_queue):
    send_order(sqs_queue, sample_order)
    messages = sqs_queue.receive_messages(MaxNumberOfMessages=1)

    process_message(messages[0])
    messages[0].delete()

    remaining = sqs_queue.receive_messages(MaxNumberOfMessages=1)
    assert remaining == []