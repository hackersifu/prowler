from unittest import mock

from providers.aws.services.directoryservice.directoryservice_service import (
    AuthenticationProtocol,
    Directory,
    RadiusSettings,
    RadiusStatus,
)

AWS_REGION = "eu-west-1"


class Test_directoryservice_radius_server_security_protocol:
    def test_no_directories(self):
        directoryservice_client = mock.MagicMock
        directoryservice_client.directories = {}
        with mock.patch(
            "providers.aws.services.directoryservice.directoryservice_service.DirectoryService",
            new=directoryservice_client,
        ):
            # Test Check
            from providers.aws.services.directoryservice.directoryservice_radius_server_security_protocol.directoryservice_radius_server_security_protocol import (
                directoryservice_radius_server_security_protocol,
            )

            check = directoryservice_radius_server_security_protocol()
            result = check.execute()

            assert len(result) == 0

    def test_directory_no_radius_server(self):
        directoryservice_client = mock.MagicMock
        directory_name = "test-directory"
        directoryservice_client.directories = {
            directory_name: Directory(
                name=directory_name,
                region=AWS_REGION,
                radius_settings=None,
            )
        }
        with mock.patch(
            "providers.aws.services.directoryservice.directoryservice_service.DirectoryService",
            new=directoryservice_client,
        ):
            # Test Check
            from providers.aws.services.directoryservice.directoryservice_radius_server_security_protocol.directoryservice_radius_server_security_protocol import (
                directoryservice_radius_server_security_protocol,
            )

            check = directoryservice_radius_server_security_protocol()
            result = check.execute()

            assert len(result) == 0

    def test_directory_radius_server_bad_auth_protocol(self):
        directoryservice_client = mock.MagicMock
        directory_name = "test-directory"
        directoryservice_client.directories = {
            directory_name: Directory(
                name=directory_name,
                region=AWS_REGION,
                radius_settings=RadiusSettings(
                    authentication_protocol=AuthenticationProtocol.MS_CHAPv1,
                    status=RadiusStatus.Completed,
                ),
            )
        }
        with mock.patch(
            "providers.aws.services.directoryservice.directoryservice_service.DirectoryService",
            new=directoryservice_client,
        ):
            # Test Check
            from providers.aws.services.directoryservice.directoryservice_radius_server_security_protocol.directoryservice_radius_server_security_protocol import (
                directoryservice_radius_server_security_protocol,
            )

            check = directoryservice_radius_server_security_protocol()
            result = check.execute()

            assert len(result) == 1
            assert result[0].resource_id == directory_name
            assert result[0].region == AWS_REGION
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == f"Radius server of Directory {directory_name} does not have recommended security protocol for the Radius server"
            )

    def test_directory_radius_server_secure_auth_protocol(self):
        directoryservice_client = mock.MagicMock
        directory_name = "test-directory"
        directoryservice_client.directories = {
            directory_name: Directory(
                name=directory_name,
                region=AWS_REGION,
                radius_settings=RadiusSettings(
                    authentication_protocol=AuthenticationProtocol.MS_CHAPv2,
                    status=RadiusStatus.Completed,
                ),
            )
        }
        with mock.patch(
            "providers.aws.services.directoryservice.directoryservice_service.DirectoryService",
            new=directoryservice_client,
        ):
            # Test Check
            from providers.aws.services.directoryservice.directoryservice_radius_server_security_protocol.directoryservice_radius_server_security_protocol import (
                directoryservice_radius_server_security_protocol,
            )

            check = directoryservice_radius_server_security_protocol()
            result = check.execute()

            assert len(result) == 1
            assert result[0].resource_id == directory_name
            assert result[0].region == AWS_REGION
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"Radius server of Directory {directory_name} have recommended security protocol for the Radius server"
            )
