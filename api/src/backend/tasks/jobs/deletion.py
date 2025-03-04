from celery.utils.log import get_task_logger
from django.db import transaction

from api.db_utils import batch_delete
from api.models import Finding, Provider, Resource, Scan

logger = get_task_logger(__name__)


def delete_provider(pk: str):
    """
    Gracefully deletes an instance of a provider along with its related data.

    Args:
        pk (str): The primary key of the Provider instance to delete.

    Returns:
        dict: A dictionary with the count of deleted objects per model,
              including related models.

    Raises:
        Provider.DoesNotExist: If no instance with the provided primary key exists.
    """
    instance = Provider.all_objects.get(pk=pk)
    deletion_summary = {}

    with transaction.atomic():
        # Delete Findings
        findings_qs = Finding.all_objects.filter(scan__provider=instance)
        _, findings_summary = batch_delete(findings_qs)
        deletion_summary.update(findings_summary)

        # Delete Resources
        resources_qs = Resource.all_objects.filter(provider=instance)
        _, resources_summary = batch_delete(resources_qs)
        deletion_summary.update(resources_summary)

        # Delete Scans
        scans_qs = Scan.all_objects.filter(provider=instance)
        _, scans_summary = batch_delete(scans_qs)
        deletion_summary.update(scans_summary)

        provider_deleted_count, provider_summary = instance.delete()
        deletion_summary.update(provider_summary)

    return deletion_summary
