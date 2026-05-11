import os
os.environ["HELPDESKHUB_DATABASE_URI"] = "sqlite:///:memory:"

from app import app, db, seed_admin_users
from models import User, Ticket, TicketHistory


def run():
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )

    with app.app_context():
        db.create_all()
        seed_admin_users()

        user = User(name="Test User", email="user@test.com", role="user")
        user.set_password("password")
        rep = User(name="Test Rep", email="rep@test.com", role="rep")
        rep.set_password("password")
        db.session.add_all([user, rep])
        db.session.commit()

    client = app.test_client()

    for path in ["/", "/login", "/register", "/admin/login"]:
        response = client.get(path)
        assert response.status_code == 200, f"{path} failed with {response.status_code}"

    response = client.post(
        "/login",
        data={"email": "user@test.com", "password": "password"},
        follow_redirects=False,
    )
    assert response.status_code == 302 and "/tickets" in response.headers["Location"]

    response = client.post(
        "/tickets/new",
        data={
            "title": "Printer down",
            "description": "Printer is not working",
            "category": "Printer",
            "priority": "High",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        ticket = Ticket.query.filter_by(title="Printer down").first()
        assert ticket is not None
        assert ticket.status == "New"
        ticket_id = ticket.id

    client.get("/logout")

    response = client.post(
        "/login",
        data={"email": "rep@test.com", "password": "password"},
        follow_redirects=False,
    )
    assert response.status_code == 302 and "/queue" in response.headers["Location"]

    response = client.post(f"/tickets/{ticket_id}/claim", follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        ticket = db.session.get(Ticket, ticket_id)
        assert ticket.assignee.email == "rep@test.com"
        assert ticket.status == "Open"
        assert TicketHistory.query.count() == 1

    response = client.post(
        f"/tickets/{ticket_id}",
        data={"action": "status", "status": "In Progress"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        ticket = db.session.get(Ticket, ticket_id)
        assert ticket.status == "In Progress"
        assert TicketHistory.query.count() == 2

    response = client.post(
        f"/tickets/{ticket_id}",
        data={"action": "status", "status": "Waiting on User"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    response = client.post(
        f"/tickets/{ticket_id}",
        data={"action": "status", "status": "Resolved"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        ticket = db.session.get(Ticket, ticket_id)
        assert ticket.status == "Resolved"
        assert TicketHistory.query.count() == 4

    response = client.post(
        f"/tickets/{ticket_id}",
        data={"action": "status", "status": "Closed"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        ticket = db.session.get(Ticket, ticket_id)
        assert ticket.status == "Closed"
        assert TicketHistory.query.count() == 5

    client.get("/logout")

    response = client.post(
        "/admin/login",
        data={"email": "admin@admin.com", "password": "admin123"},
        follow_redirects=False,
    )
    assert response.status_code == 302 and "/admin" in response.headers["Location"]

    for path in ["/admin", "/admin/users", "/admin/tickets", "/dashboard"]:
        response = client.get(path)
        assert response.status_code == 200, f"{path} failed with {response.status_code}"

    response = client.post(
        "/admin/users",
        data={
            "form_type": "create",
            "create-name": "New Agent",
            "create-email": "agent@test.com",
            "create-password": "password",
            "create-role": "rep",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        agent = User.query.filter_by(email="agent@test.com").first()
        assert agent is not None
        assert agent.role == "rep"

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    run()
