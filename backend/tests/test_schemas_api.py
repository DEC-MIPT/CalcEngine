import pytest
from pydantic import ValidationError

from app.schemas.api import (
    CalculationTypeView,
    ErrorBody,
    FieldError,
    InputView,
    OutputView,
)
from app.schemas.units import Dimension


def test_an_error_body_without_fields_leaves_them_out() -> None:
    body = ErrorBody(code="not_found", message="no stored result")

    assert body.fields is None
    assert body.model_dump(exclude_none=True) == {"code": "not_found", "message": "no stored result"}


def test_a_validation_error_body_carries_its_fields() -> None:
    body = ErrorBody(
        code="invalid_input",
        message="inputs do not fit the calculation type",
        fields=(FieldError(location=("body", "inputs", "b"), message="missing"),),
    )

    assert body.model_dump(mode="json")["fields"] == [{"location": ["body", "inputs", "b"], "message": "missing"}]


@pytest.mark.parametrize(
    "data",
    [
        {"code": "", "message": "text"},
        {"code": "not_found", "message": ""},
        {"code": "not_found", "message": "text", "extra": 1},
    ],
)
def test_an_error_body_rejects_empty_text_and_unknown_keys(data: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        ErrorBody.model_validate(data)


def test_a_field_error_needs_a_location_and_a_message() -> None:
    with pytest.raises(ValidationError):
        FieldError(location=(), message="missing")
    with pytest.raises(ValidationError):
        FieldError(location=("body",), message="")


def test_a_calculation_type_view_lists_inputs_and_outputs() -> None:
    view = CalculationTypeView(
        name="t",
        inputs=(InputView(name="b", base_unit="m", dimension=Dimension.LENGTH),),
        outputs=(OutputView(name="R", base_unit="kPa"),),
    )

    assert view.model_dump(mode="json") == {
        "name": "t",
        "inputs": [{"name": "b", "base_unit": "m", "dimension": "length"}],
        "outputs": [{"name": "R", "base_unit": "kPa"}],
    }


def test_a_view_rejects_a_unit_outside_the_vocabulary() -> None:
    with pytest.raises(ValidationError):
        OutputView(name="R", base_unit="furlong")
    with pytest.raises(ValidationError):
        InputView.model_validate({"name": "b", "base_unit": "m", "dimension": "mass"})
