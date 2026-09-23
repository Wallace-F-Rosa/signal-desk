from database.models import Base, Message


def test_message_orm_contract_matches_database_design():
    assert Message.__tablename__ == "messages"
    assert "messages" in Base.metadata.tables

    table = Base.metadata.tables["messages"]
    assert set(table.columns.keys()) == {"id", "text", "created_at", "status"}

    assert table.c.id.primary_key is True
    assert table.c.id.autoincrement is True

    assert table.c.text.nullable is False
    assert table.c.created_at.nullable is False
    assert table.c.status.nullable is False
    assert table.c.status.default.arg == "sent"
