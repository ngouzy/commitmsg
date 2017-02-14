import pytest

from commitmsg import CommitMsg, CommitSyntaxError, CommitType


def test_right_msg_with_first_line():
    # GIVEN
    msg = "feat(ui): add button"
    # WHEN
    commit_msg = CommitMsg.parse(msg)
    # THEN
    assert commit_msg.type == CommitType.feat
    assert commit_msg.scope == "ui"
    assert commit_msg.subject == "add button"
    assert commit_msg.body is None
    assert commit_msg.footer is None


def test_right_msg_with_first_line_but_without_scope():
    # GIVEN
    msg = "fix: commit-msg hook exit"
    # WHEN
    commit_msg = CommitMsg.parse(msg)
    # THEN
    assert commit_msg.type == CommitType.fix
    assert commit_msg.scope is None
    assert commit_msg.subject == "commit-msg hook exit"
    assert commit_msg.body is None
    assert commit_msg.footer is None


def test_right_msg_with_no_scope():
    # GIVEN
    msg = "feat: add button"
    # WHEN
    commit_msg = CommitMsg.parse(msg)
    # THEN
    assert commit_msg.type == CommitType.feat
    assert commit_msg.scope is None
    assert commit_msg.subject == "add button"
    assert commit_msg.body is None
    assert commit_msg.footer is None


def test_right_msg_with_first_line_and_body_():
    # GIVEN
    msg = "" + \
          "feat(ui): add button\n" + \
          "\n" + \
          "body first line\n" + \
          "body second line"
    # WHEN
    commit_msg = CommitMsg.parse(msg)
    # THEN
    assert commit_msg.type == CommitType.feat
    assert commit_msg.scope == "ui"
    assert commit_msg.subject == "add button"
    assert commit_msg.body == "body first line\nbody second line"
    assert commit_msg.footer is None


def test_right_msg_with_first_line_and_simple_body_and_simple_footer():
    # GIVEN
    msg = "feat(ui): add button\n" + \
          "\n" + \
          "body\n" + \
          "\n" + \
          "footer"
    # WHEN
    commit_msg = CommitMsg.parse(msg)
    # THEN
    assert commit_msg.type == CommitType.feat
    assert commit_msg.scope == "ui"
    assert commit_msg.subject == "add button"
    assert commit_msg.body == "body"
    assert commit_msg.footer == "footer"


def test_wrong_msg_with_first_line():
    # GIVEN
    msg = "bad message"
    # WHEN
    # THEN
    with pytest.raises(CommitSyntaxError):
        CommitMsg.parse(msg)


def test_wrong_msg_with_too_long_subject():
    # GIVEN
    msg = "feat(ui): " + "a" * (CommitMsg.FIRSTLINE_MAX_LENGTH + 1)
    # WHEN
    # THEN
    with pytest.raises(CommitSyntaxError):
        CommitMsg.parse(msg)


def test_wrong_msg_with_too_long_body():
    # GIVEN
    msg = "feat(ui): add button\n" + \
          "\n" + \
          "b" * (CommitMsg.BODY_MAX_LENGTH + 1)
    # WHEN
    # THEN
    with pytest.raises(CommitSyntaxError):
        CommitMsg.parse(msg)


def test_wrong_msg_with_too_long_footer():
    # GIVEN
    msg = "feat(ui): add button\n" + \
          "\n" + \
          "body\n" + \
          "\n" + \
          "f" * (CommitMsg.FOOTER_MAX_LENGTH + 1)
    # WHEN
    # THEN
    with pytest.raises(CommitSyntaxError):
        CommitMsg.parse(msg)


def test_wrong_msg_with_unknown_type():
    # GIVEN
    msg = "unknown(ui): add button"
    # WHEN
    # THEN
    with pytest.raises(CommitSyntaxError):
        CommitMsg.parse(msg)


def test_wrong_msg_with_bad_separator_between_firstline_and_body():
    # GIVEN
    msg = "feat(ui): add button\n" + \
          "body"
    # WHEN
    # THEN
    with pytest.raises(CommitSyntaxError):
        CommitMsg.parse(msg)