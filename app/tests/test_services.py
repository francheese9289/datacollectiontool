# tests/test_services.py
import pytest
from app import init_app, db
from models import AssessmentComponent
from services import data_analysis

@pytest.fixture
def app():
    app = init_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_assessment_name(app):
    with app.app_context():
        component = AssessmentComponent(id=1, name='Test Component', score=100)
        db.session.add(component)
        db.session.commit()
        assert data_analysis.get_assessment_name(1) == 'Test Component'
        assert data_analysis.get_assessment_name(2) is None
