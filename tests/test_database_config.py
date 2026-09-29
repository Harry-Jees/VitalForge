import re
from pathlib import Path

from config import MYSQL_DATABASE


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_database_is_fixed_to_defaultdb():
    assert MYSQL_DATABASE == "defaultdb"


def test_schema_does_not_create_or_switch_databases():
    schema = (PROJECT_ROOT / "database" / "schema.sql").read_text(encoding="utf-8")
    assert not re.search(r"(?im)^\s*(?:CREATE\s+DATABASE\b|USE\b)", schema)
