from app.services.agent_tools import AgentTools


def test_keywords():
    tools = AgentTools()
    result = tools.extract_keywords("学生请假需要填写申请表，提交医院证明，并联系辅导员审批。")
    assert result
