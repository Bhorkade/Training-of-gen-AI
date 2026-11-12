
from dataclasses import dataclass, asdict, field

def clean_value(value):
    if value is None:
        return ""
    return str(value).strip()

@dataclass
class Record:
    id: str
    title: str
    category: str
    description: str
    eligibility: str
    source: str
    extra_fields: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, row, row_number=1):
        # Normalize CSV column names
        values = {
            str(key).strip().lower().replace(" ", "_"): clean_value(value)
            for key, value in row.items()
            if key is not None
        }

        def get_value(*names):
            for name in names:
                if values.get(name):
                    return values[name]
            return ""

        known_columns = {
            "id", "record_id", "serial_no", "sr_no",
            "title", "name", "scheme_name", "startup_name",
            "company_name",
            "category", "sector", "industry", "state", "type",
            "description", "details", "scheme_description",
            "eligibility", "eligibility_criteria", "criteria",
            "source", "source_url", "url", "link"
        }

        # Keep all other CSV columns as separate fields
        extra_fields = {
            key: value
            for key, value in values.items()
            if key not in known_columns
        }

        return cls(
            id=get_value("id", "record_id", "serial_no", "sr_no")
               or str(row_number),

            title=get_value(
                "title", "name", "scheme_name",
                "startup_name", "company_name"
            ) or "Untitled Record",

            category=get_value(
                "category", "sector", "industry", "state", "type"
            ) or "General",

            # Only actual description columns go here
            description=get_value(
                "description", "details", "scheme_description"
            ),

            eligibility=get_value(
                "eligibility", "eligibility_criteria", "criteria"
            ),

            source=get_value(
                "source", "source_url", "url", "link"
            ),

            extra_fields=extra_fields
        )

    def to_dict(self):
        result = asdict(self)
        extra_fields = result.pop("extra_fields")
        result.update(extra_fields)
        return result