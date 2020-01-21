import os

from datadog_checks.base.ddyaml import safe_yaml_load

try:
    from datadog_test_libs.win.pdh_mocks import (  # noqa: F401
        initialize_pdh_tests,
        pdh_mocks_fixture_bad_perf_strings,
        pdh_mocks_fixture,
    )
except ImportError:
    import platform

    if platform.system() != 'Windows':
        pass


FIXTURE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fixtures', 'wmi')


def test_filter_yaml(mock_filter_sampler, aggregator, check):
    conf = os.path.join(FIXTURE_PATH, "wmi.yaml")
    with open(conf) as f:
        stream = f.read()
        yaml_config = safe_yaml_load(stream)

        instance = yaml_config.get('instances')[0]
        check.check(instance)

        # the only metric that matches the filter
        aggregator.assert_metric("proc.cpu_pct", count=1)
