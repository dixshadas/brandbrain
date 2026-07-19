"""The ten services. Each is a self-contained package with the same shape:

    schemas.py     Pydantic request/response + internal DTOs (the sync contract)
    interface.py   The service Protocol other modules depend on (never the impl)
    service.py     The implementation (stubbed in this scaffold)
    models.py      SQLAlchemy tables it owns (data-heavy services only)
    repository.py  Data access, brand-scoped (data-heavy services only)
    api.py         FastAPI router (mounted by main.create_app)
    events.py      Events it PUBLISHES and CONSUMES (the async contract)

A service may call another only through its interface (in-process) or by publishing an event.
No service reaches into another's tables. That rule is what makes extraction to a microservice a
mechanical move later.
"""
