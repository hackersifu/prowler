from lib.check.models import Check, Check_Report
from providers.aws.services.directoryservice.directoryservice_client import (
    directoryservice_client,
)


class directoryservice_directory_log_forwarding_enabled(Check):
    def execute(self):
        findings = []
        for directory in directoryservice_client.directories.values():
            report = Check_Report(self.metadata)
            report.region = directory.region
            report.resource_id = directory.name
            if directory.log_subscriptions:
                report.status = "PASS"
                report.status_extended = f"Directory Service {directory.name} have log forwarding to CloudWatch enabled"
            else:
                report.status = "FAIL"
                report.status_extended = f"Directory Service {directory.name} have log forwarding to CloudWatch disabled"

            findings.append(report)

        return findings
