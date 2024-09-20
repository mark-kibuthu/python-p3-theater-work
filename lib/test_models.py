import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Role, Audition  # Ensure both Role and Audition are imported

@pytest.fixture(scope="function")
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_role_methods(session):
    # Create sample data
    role1 = Role(character_name="Hamlet")
    audition1 = Audition(actor="John Doe", location="New York", phone=123456789, hired=False, role=role1)
    audition2 = Audition(actor="Jane Smith", location="Los Angeles", phone=987654321, hired=True, role=role1)
    audition3 = Audition(actor="Alice Brown", location="Boston", phone=111111111, hired=True, role=role1)
    
    session.add_all([role1, audition1, audition2, audition3])
    session.commit()

    # Query to check if data is there
    roles = session.query(Role).all()
    auditions = session.query(Audition).all()
    print("Roles:", [role.character_name for role in roles])
    print("Auditions:", [(audition.actor, audition.hired) for audition in auditions])

    # Test Role.actors()
    assert role1.actors() == ["John Doe", "Jane Smith", "Alice Brown"]

    # Test Role.locations()
    assert role1.locations() == ["New York", "Los Angeles", "Boston"]

    # Test Role.lead()
    lead = role1.lead()
    assert lead.actor == "Jane Smith"

    # Test Role.understudy()
    understudy = role1.understudy()
    assert understudy.actor == "Alice Brown"

def test_audition_methods(session):
    # Create sample data
    role1 = Role(character_name="Ophelia")
    audition1 = Audition(actor="Mark Johnson", location="Chicago", phone=555555555, hired=False, role=role1)
    
    session.add(role1)
    session.add(audition1)
    session.commit()

    # Query to check if data is there
    roles = session.query(Role).all()
    auditions = session.query(Audition).all()
    print("Roles:", [role.character_name for role in roles])
    print("Auditions:", [(audition.actor, audition.hired) for audition in auditions])

    # Test Audition.role
    assert audition1.role.character_name == "Ophelia"

    # Test Audition.call_back()
    audition1.call_back()
    session.commit()
    assert audition1.hired == True
