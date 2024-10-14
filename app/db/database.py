from sqlmodel import Session, SQLModel, create_engine
from fastapi import Depends
from sqlmodel import Session
from typing import Annotated

from app.config import settings
from app.models.requirements import Requirement, RequirementStatus, RequirementGroup


connect_args = {"check_same_thread": False}

engine = create_engine(settings.database_engine, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    if settings.environment == "development":
        add_test_data()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


# Test data
def add_test_data():
    requirement_groups_data = [
        {"name": "Base Security Controls", "description": "Basic security controls for all projects."},
        {"name": "DevSecOps Maturity Model", "description": "Requirements to achieve DevSecOps maturity."},
        {"name": "Compliance", "description": "Requirements for regulatory compliance."}
    ]

    requirements_data = [
        {"name": "TLS v1.2 or above is required.", "description": "Ensure secure communication.", "status": RequirementStatus.MET,
         "acceptance_criteria": "Connections use at least TLS v1.2.", "group_name": "Base Security Controls"},
        
        {"name": "Static Analysis Security Testing is enabled.", "description": "SAST is enabled.", "status": RequirementStatus.MET,
         "acceptance_criteria": "Scanning is done via the CI/CD pipeline.", "group_name": "DevSecOps Maturity Model"},
        
        {"name": "Software Composition Analysis is enabled.", "description": "SCA is enabled.", "status": RequirementStatus.NOT_MET,
         "acceptance_criteria": "SCA is included in build pipeline.", "group_name": "DevSecOps Maturity Model"},
        
        {"name": "Data encryption at rest.", "description": "Sensitive data must be encrypted.", "status": RequirementStatus.NOT_MET,
         "acceptance_criteria": "Encryption algorithms approved by standards.", "group_name": "Compliance"},
        
        {"name": "Multi-Factor Authentication (MFA) is enforced.", "description": "MFA for all users.", "status": RequirementStatus.MET,
         "acceptance_criteria": "All logins require MFA.", "group_name": "Base Security Controls"},
        
        # Additional requirements can be added here
    ]

    # Initialize the database with the sample data
    with Session(engine) as session:
        # Add requirement groups to the database
        requirement_groups = {}
        for group_data in requirement_groups_data:
            group = RequirementGroup(**group_data)
            session.add(group)
            session.commit()
            session.refresh(group)
            requirement_groups[group.name] = group

        # Add requirements to the database
        for req_data in requirements_data:
            group_name = req_data.pop("group_name")
            group = requirement_groups[group_name]
            requirement = Requirement(**req_data, group_id=group.id)
            session.add(requirement)

        # Commit all changes
        session.commit()
    # groups = [
    #     RequirementGroup("Base Security Controls", "Base security controls for our organization."),
    #     RequirementGroup("Software Development", "Code development security controls.")
    # ]
    # requirements = [
    #     Requirement(
    #         name="TLS version requirement",
    #         description="TLS v1.2 or above is required.",
    #         group="Base Security Controls",
    #         status=RequirementStatus.MET,
    #         acceptance_criteria="Verified with the latest scan.",
    #     ),
    #     Requirement(
    #         name="SAST is enabled",
    #         description="Static Analysis Security Testing is required.",
    #         group="Software Development",
    #         status=RequirementStatus.MET,
    #         acceptance_criteria="SAST is included in the CI/CD pipeline.",
    #     ),
    #     Requirement(
    #         name="Endpoint protection",
    #         description="Endpoints must be protected with antivirus software.",
    #         group="Base Security Controls",
    #         status=RequirementStatus.MET,
    #         acceptance_criteria="Antivirus is installed on all company devices.",
    #     ),
    #     Requirement(
    #         name="Data encryption",
    #         description="All sensitive data must be encrypted at rest and in transit.",
    #         group="Software Development",
    #         status=RequirementStatus.MET,
    #         acceptance_criteria="Encryption verified via audit.",
    #     ),
    #     Requirement(
    #         name="Multi-factor authentication",
    #         description="MFA is required for all user accounts.",
    #         group="Software Development",
    #         status=RequirementStatus.MET,
    #         acceptance_criteria="MFA policy is enforced in the identity provider.",
    #     ),
    #     Requirement(
    #         name="Patch management",
    #         description="Systems must be patched within 30 days of a security update.",
    #         group="Base Security Controls",
    #         status=RequirementStatus.MET,
    #         acceptance_criteria="Patches applied within the required time frame.",
    #     ),
    #     Requirement(
    #         name="Code review process",
    #         description="All code changes must go through peer review.",
    #         group="Software Development",
    #         status=RequirementStatus.MET,
    #         acceptance_criteria="Pull requests are reviewed by at least one other developer.",
    #     ),
    #     Requirement(
    #         name="Access logging",
    #         description="Access to sensitive data must be logged and monitored.",
    #         group="Base Security Controls",
    #         status=RequirementStatus.NOT_MET,
    #         acceptance_criteria="Logs are collected and reviewed weekly.",
    #     ),
    #     Requirement(
    #         name="Network segmentation",
    #         description="Sensitive network segments must be isolated from the rest of the network.",
    #         group="Software Development",
    #         status=RequirementStatus.NOT_MET,
    #         acceptance_criteria="Segmentation reviewed and approved.",
    #     ),
    #     Requirement(
    #         name="Incident response plan",
    #         description="An incident response plan must be documented and tested annually.",
    #         group="Software Development",
    #         status=RequirementStatus.MET,
    #         acceptance_criteria="Plan was tested in the last 12 months.",
    #     ),
    #     Requirement(
    #         name="Third-party risk assessment",
    #         description="Third-party vendors must undergo risk assessments before onboarding.",
    #         group="Software Development",
    #         status=RequirementStatus.MET,
    #         acceptance_criteria="Risk assessments are completed for all new vendors.",
    #     ),
    #     Requirement(
    #         name="Backup and recovery",
    #         description="Critical data must be backed up and tested for recovery regularly.",
    #         group="Software Development",
    #         status=RequirementStatus.NOT_MET,
    #         acceptance_criteria="Backup and recovery tests performed quarterly.",
    #     ),
    # ]

    # # Open a session and add the test data
    # with Session(engine) as session:
    #     session.add_all(groups)
    #     session.commit()
    #     session.add_all(requirements)
    #     session.commit()

